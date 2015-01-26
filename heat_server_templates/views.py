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

from openstack_dashboard.dashboards.project.stacks.views import CreateStackView

from heat_server_templates.utils import get_templates, get_environments, \
    get_template_data, get_environment_data, CustomEncoder



class SelectTemplateView(forms.ModalFormView):
    form_class = LocalTemplateStackForm
    template_name = 'project/stacks/select_template.html'
    success_url = reverse_lazy('horizon:project:stacks:index')

    def get_form_kwargs(self):
        kwargs = super(SelectTemplateView, self).get_form_kwargs()
        kwargs['next_view'] = CreateStackView
        return kwargs