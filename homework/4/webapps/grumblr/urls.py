__author__ = 'jianheluo'

from django.conf.urls import include, url
from . import views


urlpatterns = [

    # empty url
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'grumblr/login.html'}, name='login'),

    # new argument 'template_name'
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'grumblr/login.html'}),

    # url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'grumblr.views.my_logout', name='logout'),

    # registration is normal route
    url(r'^registration/$', 'grumblr.views.registration', name='registration'),

    # this is the home page urls
    url(r'^home/$', 'grumblr.views.home', name='home'),

    url(r'^post_message_home_page/$', 'grumblr.views.post_message_home_page', name='post_message_home_page'),

    url(r'^profile/', 'grumblr.views.profile', name='profile'),
    url(r'^post_message_profile_page/$', 'grumblr.views.post_message_profile_page', name='post_message_profile_page'),

    url(r'^other_profile/(?P<user_id>\d+)$', 'grumblr.views.other_user_profile', name='other_profile'),


    url(r'^edit_profile/$', 'grumblr.views.go_to_profile_edit_page', name='go_to_profile_edit_page'),


    url(r'^change_password/$', 'grumblr.views.go_to_password_change_page', name='go_to_password_change_page'),
    url(r'^update_password/$', 'grumblr.views.update_password', name='update_password'),


    # define url for getting photo
    url(r'^photo/$', 'grumblr.views.get_photo', name='get_photo'),
    url(r'^other_photo_abc/(?P<id>\d+)$', 'grumblr.views.get_other_photo', name='get_other_photo'),

    url(r'^friends/$', 'grumblr.views.get_friends_stream', name='get_friends_stream'),


    url(r'^follow/$', 'grumblr.views.follow', name='follow'),
    url(r'^unfollow/$', 'grumblr.views.unfollow', name='unfollow'),

    url(r'^reset_password/$', 'grumblr.views.reset_password', name='reset_password'),


]