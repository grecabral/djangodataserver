from django.conf.urls import url

from . import views

app_name = 'hello'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^json_post/$', views.json_post, name='json_post'),
]