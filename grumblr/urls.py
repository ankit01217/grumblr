from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views
from grumblr.forms import *
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from webapps import settings

login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), settings.LOGIN_REDIRECT_URL)

urlpatterns = [
    url(r'^$', views.home, name = "home"),
 	url(r'^register/$', views.register, name = "register"),
 	url(r'^friendstream/$', views.friend_stream, name = "friendstream"),
 	url(r'^globalstream/$', views.global_stream, name = "globalstream"),
 	url(r'^compose/$', views.compose, name = "compose"),
 	url(r'^profile/(?P<id>\d+)/$', views.profile, name = "profile"),
 	url(r'^change_avatar/$', views.change_avatar, name = "change_avatar"),
 	url(r'^follow/(?P<id>\d+)/$', views.follow_profile, name = "follow"),
 	url(r'^confirm_registration/(?P<username>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.confirm_registration, name = "confirm"),
 	url(r'^comments/$', views.add_comment, name = "comment"),
 	
 	url(r'^login/$', login_forbidden(auth_views.login) , {'template_name':'login.html', 'authentication_form':LoginForm}, name = "login"),
 	url(r'^logout/$', auth_views.logout , {'template_name':'login.html'}, name = "logout"),
 	url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'password_reset.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),
    url('^password_change/$', auth_views.password_change, {'template_name': 'password_change.html'}, name= 'password_change'),                           
    url('^password_change/done/$', auth_views.password_change, {'template_name': 'password_change_done.html'}, name= 'password_change_done'),                             
 	
 	#json data urls
 	url(r'^globalstream/json/$', views.global_stream_json , name = "global_stream_json"),
 	url(r'^friendstream/json/$', views.friend_stream_json , name = "friend_stream_json"),
 	url(r'^profile/(?P<id>\d+)/json/$', views.profile_posts_json , name = "profile_posts_json"),
 			
]
