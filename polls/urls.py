from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<poll_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^user_page/$', views.user_page, name='user_page'),
    (r'^accounts/', include('allauth.urls')),
)
