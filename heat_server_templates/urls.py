from django.conf.urls import patterns
from django.conf.urls import url

from heat_server_templates import views

urlpatterns = patterns(
    '',
    url(r'^select_template$',
        views.SelectTemplateView.as_view(),
        name='select_template'),
)
"""
url(r'^edit_template$',
    views.UpdateTemplateParamsView.as_view(), name='edit_template'),
"""