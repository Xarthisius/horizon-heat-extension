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

from .forms import LocalTemplateStackForm, LocalTemplateChangeForm

from heat_server_templates.utils import get_templates, get_environments, \
    get_template_data, get_environment_data, CustomEncoder


class SelectTemplateView(forms.ModalFormView):
    form_class = LocalTemplateStackForm
    template_name = 'project/stacks/select_template.html'
    success_url = reverse_lazy('horizon:project:heat_templates:edit_template')

    def get_form_kwargs(self):
        kwargs = super(SelectTemplateView, self).get_form_kwargs()
        kwargs['next_view'] = UpdateTemplateParamsView
        return kwargs


class UpdateTemplateParamsView(forms.ModalFormView):
    form_class = LocalTemplateChangeForm
    template_name = 'project/stacks/update_template.html'
    success_url = reverse_lazy('horizon:project:stacks:index')

    def get_context_data(self, **kwargs):
        context = super(UpdateTemplateParamsView, self).get_context_data(**kwargs)

        context["template"] = self.kwargs.get("template", self.request.POST["template"])
        context["stack_name"] = self.kwargs.get("stack_name", self.request.POST["stack_name"])
        context["timeout_mins"] = self.kwargs.get("timeout_mins", self.request.POST["timeout_mins"])
        context["disable_rollback"] = self.kwargs.get("disable_rollback", self.request.POST.get("disable_rollback", False))

        context["parameters"] = self.kwargs.get("parameters", self.request.POST["parameters"])

        return context

    def get_initial(self):
        context = self.get_context_data()
        return {'template': context["template"],
                'parameters': context["parameters"],
                'stack_name': context["stack_name"],
                'timeout_mins': context["timeout_mins"],
                'disable_rollback': context["disable_rollback"],
                }
