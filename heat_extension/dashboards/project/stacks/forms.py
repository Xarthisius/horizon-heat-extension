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
# allow url, raw and file inputs
# prevent user fail
HEAT_LOCAL_ONLY = getattr(settings, "HEAT_LOCAL_ONLY", True)
HIDE_SOURCE = getattr(settings, "HIDE_SOURCE", True)


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


class LocalTemplateStackForm(forms.SelfHandlingForm):

    class Meta:
        name = _('Launch Template')
        help_text = _('From here you can select and launch a template.')

    template_data = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False)

    environment_data = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False)

    parameters = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False)

    stack_name = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False)

    timeout_mins = forms.IntegerField(
        initial=60,
        label=_('Creation Timeout (minutes)'),
        help_text=_('Stack creation timeout in minutes.'),
        required=True)

    enable_rollback = forms.BooleanField(
        label=_('Rollback On Failure'),
        help_text=_('Enable rollback on create/update failure.'),
        required=False)

    attributes = {'class': 'switchable', 'data-slug': 'localsource'}
    choices = get_templates()
    template = forms.ChoiceField(label=_('Template'),
                                 choices=choices,
                                 widget=forms.Select(attrs=attributes),
                                 required=True)

    def __init__(self, request, *args, **kwargs):
        self.next_view = kwargs.pop('next_view')
        super(LocalTemplateStackForm, self).__init__(request, *args, **kwargs)

        if HEAT_LOCAL:
            for template in get_templates():
                attributes = create_upload_form_attributes(
                    'local',
                    '%s' % template[0],
                    _('Environment'))
                field = forms.ChoiceField(label=_('Environment'),
                                          choices=get_environments(
                                              template[0]),
                                          widget=forms.Select(
                                              attrs=attributes),
                                          required=False)
                self.fields["environment____%s" % template[0]] = field

    def clean(self):
        cleaned = super(LocalTemplateStackForm, self).clean()
        template_name = cleaned["template"]
        cleaned["template_data"] = get_template_data(template_name)
        cleaned["environment_data"] = get_environment_data(
            template_name, cleaned["environment____%s" % template_name])

        cleaned['stack_name'] = "%s_%s" % (cleaned["template"], cleaned["environment____%s" % cleaned["template"]])

        # Validate the template and get back the params.
        kwargs = {}
        kwargs['template'] = cleaned["template_data"]

        try:
            validated = api.heat.template_validate(self.request, **kwargs)
            cleaned["parameters"] = validated
        except Exception as e:
            raise forms.ValidationError(unicode(e))

        return cleaned

    def handle(self, request, data):
        kwargs = self.create_kwargs(data)

        fields = {
            'stack_name': data.get('stack_name'),
            'template': data.get('template_data'),
            'environment': data.get('environment_data'),
            'timeout_mins': data.get('timeout_mins'),
            'disable_rollback': not(data.get('enable_rollback')),
            'parameters': {},
#            'password': data.get('password')
        }

        try:
            api.heat.stack_create(self.request, **fields)
            messages.success(request, _("Stack creation started."))
            return True
        except Exception:
            exceptions.handle(request)
