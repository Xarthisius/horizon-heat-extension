import json
import logging

from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables  # noqa
from django.conf import settings
from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api

from heat_extension.utils import get_templates, get_environments, \
    get_template_data, get_environment_data

LOG = logging.getLogger(__name__)

HEAT_LOCAL = getattr(settings, "HEAT_LOCAL", True)
HEAT_ALLOW_OWN = getattr(settings, "HEAT_ALLOW_OWN", False) # allow url, raw and file inputs

def create_upload_form_attributes(prefix, input_type, name):
    """Creates attribute dicts for the switchable upload form

    :type prefix: str
    :param prefix: prefix (environment, template) of field
    :type input_type: str
    :param input_type: field type (file, raw, url)
    :type name: str
    :param name: translated text label to display to user
    :rtype: dict
    :return: an attribute set to pass to form build
    """
    attributes = {'class': 'switched', 'data-switch-on': prefix + 'source'}
    attributes['data-' + prefix + 'source-' + input_type] = name
    return attributes


class CustomTemplateForm(forms.SelfHandlingForm):

    class Meta:
        name = _('Select Template')
        help_text = _('From here you can select a template to launch '
                      'a stack.')

    choices = []

    if HEAT_ALLOW_OWN:
        choices.append(('url', _('URL')))
        choices.append(('file', _('File')))
        choices.append(('raw', _('Direct Input')))

    if HEAT_LOCAL:
        choices.append(('storage', _('Local Storage')))
        #choices = reversed(choices) # make it default

    attributes = {'class': 'switchable', 'data-slug': 'templatesource'}
    template_source = forms.ChoiceField(label=_('Template Source'),
                                        choices=choices,
                                        widget=forms.Select(attrs=attributes))

    template_choices = get_templates()

    attributes = create_upload_form_attributes(
        'template',
        'storage',
        _('Template File'))

    template_storage_source = forms.ChoiceField(label=_('Template File'),
                                        choices=template_choices,
                                        widget=forms.Select(attrs=attributes),
                                        required=False)

    attributes = create_upload_form_attributes(
        'template',
        'file',
        _('Template File'))
    template_upload = forms.FileField(
        label=_('Template File'),
        help_text=_('A local template to upload.'),
        widget=forms.FileInput(attrs=attributes),
        required=False)

    attributes = create_upload_form_attributes(
        'template',
        'url',
        _('Template URL'))
    template_url = forms.URLField(
        label=_('Template URL'),
        help_text=_('An external (HTTP) URL to load the template from.'),
        widget=forms.TextInput(attrs=attributes),
        required=False)

    attributes = create_upload_form_attributes(
        'template',
        'raw',
        _('Template Data'))
    template_data = forms.CharField(
        label=_('Template Data'),
        help_text=_('The raw contents of the template.'),
        widget=forms.widgets.Textarea(attrs=attributes),
        required=False)

    attributes = {'data-slug': 'envsource', 'class': 'switchable'}

    environment_source = forms.ChoiceField(
        label=_('Environment Source'),
        choices=choices,
        widget=forms.Select(attrs=attributes),
        required=False)

    environment_choices = get_environments()

    attributes = create_upload_form_attributes(
        'env',
        'storage',
        _('Environment File'))

    environment_storage_source = forms.ChoiceField(label=_('Environment File'),
                                        choices=environment_choices,
                                        widget=forms.Select(attrs=attributes),
                                        required=False)

    attributes = create_upload_form_attributes(
        'env',
        'file',
        _('Environment File'))
    environment_upload = forms.FileField(
        label=_('Environment File'),
        help_text=_('A local environment to upload.'),
        widget=forms.FileInput(attrs=attributes),
        required=False)

    attributes = create_upload_form_attributes(
        'env',
        'url',
        _('Environment URL'))
    environment_url = forms.URLField(
        label=_('Environment URL'),
        help_text=_('An external (HTTP) URL to load the environment from.'),
        widget=forms.TextInput(attrs=attributes),
        required=False)

    attributes = create_upload_form_attributes(
        'env',
        'raw',
        _('Environment Data'))
    environment_data = forms.CharField(
        label=_('Environment Data'),
        help_text=_('The raw contents of the environment file.'),
        widget=forms.widgets.Textarea(attrs=attributes),
        required=False)

    def __init__(self, *args, **kwargs):
        self.next_view = kwargs.pop('next_view')
        super(CustomTemplateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned = super(CustomTemplateForm, self).clean()

        if not cleaned['template_storage_source']:
            files = self.request.FILES
            self.clean_uploaded_files('template', _('template'), cleaned, files)
            self.clean_uploaded_files('environment',
                _('environment'),
                cleaned,
                files)
        else:
            # load from file
            cleaned["template_data"] = get_template_data(cleaned["template_storage_source"])

        # Validate the template and get back the params.
        kwargs = {}
        if cleaned['template_data']:
            kwargs['template'] = cleaned['template_data']
        else:
            kwargs['template_url'] = cleaned['template_url']

        try:
            validated = api.heat.template_validate(self.request, **kwargs)
            cleaned['template_validate'] = validated
        except Exception as e:
            raise forms.ValidationError(unicode(e))

        return cleaned

    def clean_uploaded_files(self, prefix, field_label, cleaned, files):
        """Cleans Template & Environment data from form upload.

        Does some of the crunchy bits for processing uploads vs raw
        data depending on what the user specified. Identical process
        for environment data & template data.

        :type prefix: str
        :param prefix: prefix (environment, template) of field
        :type field_label: str
        :param field_label: translated prefix str for messages
        :type input_type: dict
        :param prefix: existing cleaned fields from form
        :rtype: dict
        :return: cleaned dict including environment & template data
        """

        upload_str = prefix + "_upload"
        data_str = prefix + "_data"
        url = cleaned.get(prefix + '_url')
        data = cleaned.get(prefix + '_data')

        has_upload = upload_str in files
        # Uploaded file handler
        if has_upload and not url:
            log_template_name = files[upload_str].name
            LOG.info('got upload %s' % log_template_name)

            tpl = files[upload_str].read()
            if tpl.startswith('{'):
                try:
                    json.loads(tpl)
                except Exception as e:
                    msg = _('There was a problem parsing the'
                            ' %(prefix)s: %(error)s')
                    msg = msg % {'prefix': prefix, 'error': e}
                    raise forms.ValidationError(msg)
            cleaned[data_str] = tpl

        # URL handler
        elif url and (has_upload or data):
            msg = _('Please specify a %s using only one source method.')
            msg = msg % field_label
            raise forms.ValidationError(msg)

        elif prefix == 'template':
            # Check for raw template input - blank environment allowed
            if not url and not data:
                msg = _('You must specify a template via one of the '
                        'available sources.')
                raise forms.ValidationError(msg)

    def create_kwargs(self, data):
        kwargs = {'parameters': data['template_validate'],
                  'environment_url': data['environment_url'],
                  'template_data': data['template_data'],
                  'template_url': data['template_url']}

        # load environment data          
        if not HEAT_LOCAL:
            kwargs["environment_data"] = data['environment_data']
        else:
            kwargs["environment_data"] = get_environment_data(data["environment_storage_source"])

        if data.get('stack_id'):
            kwargs['stack_id'] = data['stack_id']
        return kwargs

    def handle(self, request, data):
        kwargs = self.create_kwargs(data)
        # NOTE (gabriel): This is a bit of a hack, essentially rewriting this
        # request so that we can chain it as an input to the next view...
        # but hey, it totally works.
        request.method = 'GET'

        return self.next_view.as_view()(request, **kwargs)


class CustomChangeTemplateForm(CustomTemplateForm):
    class Meta:
        name = _('Edit Template')
        help_text = _('From here you can select a new template to re-launch '
                      'a stack.')
    stack_id = forms.CharField(label=_('Stack ID'),
        widget=forms.widgets.HiddenInput,
        required=True)
    stack_name = forms.CharField(label=_('Stack Name'),
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        ))