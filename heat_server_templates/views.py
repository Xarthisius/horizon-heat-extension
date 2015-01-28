# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import logging
from operator import attrgetter

import yaml

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
import django.views.generic

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon.utils import memoized

LOG = logging.getLogger(__name__)

from .forms import LocalTemplateStackForm

#from openstack_dashboard.dashboards.project.stacks.views import CreateStackView
from openstack_dashboard.dashboards.project.stacks.forms import CreateStackForm

from heat_server_templates.utils import get_templates, get_environments, \
    get_template_data, get_environment_data, CustomEncoder

class CreateStackView(forms.ModalFormView):
    form_class = CreateStackForm
    template_name = 'project/stacks/create.html'
    success_url = reverse_lazy('horizon:project:stacks:index')

    def get_initial(self):
        initial = {}
        self.load_kwargs(initial)
        if 'parameters' in self.kwargs:
            initial['parameters'] = json.dumps(self.kwargs['parameters'])
        initial["stack_name"] = self.kwargs["stack_name"] # ugly fix
        return initial

    def load_kwargs(self, initial):
        # load the "passed through" data from template form
        for prefix in ('template', 'environment'):
            for suffix in ('_data', '_url'):
                key = prefix + suffix
                if key in self.kwargs:
                    initial[key] = self.kwargs[key]

    def get_form_kwargs(self):
        kwargs = super(CreateStackView, self).get_form_kwargs()
        if 'parameters' in self.kwargs:
            kwargs['parameters'] = self.kwargs['parameters']
        else:
            data = json.loads(self.request.POST['parameters'])
            kwargs['parameters'] = data
        return kwargs


class SelectTemplateView(forms.ModalFormView):
    form_class = LocalTemplateStackForm
    template_name = 'project/stacks/select_template.html'
    success_url = reverse_lazy('horizon:project:stacks:index')

    def get_form_kwargs(self):
        kwargs = super(SelectTemplateView, self).get_form_kwargs()
        kwargs['next_view'] = CreateStackView
        return kwargs

