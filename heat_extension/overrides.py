import horizon
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from openstack_dashboard.dashboards.project. \
     stacks.views import SelectTemplateView, ChangeTemplateView

from heat_extension.dashboards.project.stacks.forms \
     import CustomTemplateForm, CustomChangeTemplateForm


SelectTemplateView.form_class = CustomTemplateForm
ChangeTemplateView.form_class = CustomChangeTemplateForm

# noqa | support for other overrides

"""
def auto_overrides(app):
    module_name = "%s.%s" % (app, "overrides")
    try:
        mod = __import__(module_name)
    except Exception, e:
        pass

for app in settings.INSTALLED_APPS:
    auto_overrides(app)
"""