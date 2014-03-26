from django.conf.urls import patterns, url

from vmm import views

urlpatterns = patterns('',
    # Generic views
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<primary_name>\w+)', views.detail, name='detail'),
    # Creation, termination etc
    url(r'^create/$', views.create, name='create'),
    url(r'^terminate/(?P<instance_id>[\w\-]+)', views.terminate, name='terminate'),
    url(r'^poweron/(?P<instance_id>[\w\-]+)', views.poweron, name='poweron'),
    url(r'^poweroff/(?P<instance_id>[\w\-]+)', views.poweroff, name='poweroff'),
    # Ajax views
    url(r'^vmstatus/$', views.vmstatus, name='vmstatus'),
    url(r'^vmstatus/(?P<primary_name>[\w\-]+)', views.vmstatus, name='vmstatus'),
    # Not quite an ajax view, but checked by the puppetmaster certsign daemon
    # Should return epoch time when VM has been created or 0 if VM doesn't exist
    url(r'^vmcreatedtime/(?P<primary_name>[\w\-]+)', views.vmcreatedtime, name='vmcreatedtime'),
    # Background tasks
    url(r'^refresh_local_state/$', views.refresh_local_state, name='refresh_local_state'),
    url(r'^refresh_local_state/(?P<instance_id>[\w\-]+)', views.refresh_local_state, name='refresh_local_state'),
)
