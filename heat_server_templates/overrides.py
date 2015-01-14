import horizon
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from openstack_dashboard.dashboards.project. \
     stacks.views import SelectTemplateView

from openstack_dashboard.dashboards.project. \
     stacks.tables import LaunchStack

from heat_server_templates.forms import LocalTemplateStackForm


SelectTemplateView.form_class = LocalTemplateStackForm
#SelectTemplateView.success_url = reverse_lazy('horizon:project:stacks:index')

LaunchStack.url =  "horizon:project:heat_templates:select_template"
