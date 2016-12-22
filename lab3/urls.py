"""lab3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from serials.views import *
from django.contrib.auth import views

urlpatterns = [
    url('^$', SerialsView.as_view()),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', logout_view),
    url(r'^registration/$', RegistrationView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^my_serials/$', MySerialsView.as_view()),
    url(r'^serials/$', SerialsView.as_view()),
    url(r'^serials/(\d+)/$', SerialView.as_view()),
    url(r'^serials/(\d+)/start_watch/$', SerialView.start_watch),
    url(r'^serials/(\d+)/stop_watch/$', SerialView.stop_watch),
    url(r'^serials/(\d+)/episodes/$', EpisodesView.as_view()),
    url(r'^episode/(\d+)/$', EpisodeView.as_view()),
    url(r'^episode/(\d+)/check/$', EpisodeView.check_as_watched),
    url(r'^my_episodes/$', MyEpisodesView.as_view()),
    url(r'^parse/$', parse),
    url(r'^parse2/$', parse2),
]
