import horizon
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from openstack_dashboard.dashboards.project. \
     stacks.views import SelectTemplateView

from heat_extension.dashboards.project.stacks.forms \
     import LocalTemplateStackForm

SelectTemplateView.form_class = LocalTemplateStackForm
