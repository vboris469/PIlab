from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import FormView
from serials.models import *
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
import serials.parser


class SerialsView(View):

    def get(self, request):
        serials = Serial.objects.all()
        return render(request, 'serials_list.html', {'serials': serials})


class MySerialsView(LoginRequiredMixin, View):

    def get(self, request):
        serials = []
        for watching in request.user.watching.all():
            serials.append(watching.serial)
        return render(request, 'serials_list.html', {'serials': serials})


class SerialView(View):

    def get(self, request, pk):
        serial = get_object_or_404(Serial, pk=pk)
        watching = request.user.watching.filter(serial=pk).count()
        comments = Comment.objects.filter(page=request.path)
        return render(request, 'serial.html', {'serial': serial, 'watching': watching, 'comments': comments})

    def post(self, request, pk):
        if not request.user.pk:
            return HttpResponseRedirect('/login/')
        comment = Comment()
        comment.user_name = request.user.username
        comment.text = request.POST['text']
        comment.page = request.path
        comment.save()
        return self.get(request, pk)

    @staticmethod
    @login_required
    def start_watch(request, pk):
        watching = request.user.watching.filter(serial=pk).count()
        if not watching:
            watching = SerialWatching()
            watching.user = request.user
            watching.serial = get_object_or_404(Serial, pk=pk)
            watching.save()
        return HttpResponseRedirect('/serials/' + pk + '/')

    @staticmethod
    @login_required
    def stop_watch(request, pk):
        watching = request.user.watching.filter(serial=pk)
        for w in watching:
            w.delete()
        return HttpResponseRedirect('/serials/' + pk + '/')


class EpisodesView(View):

    def get(self, request, pk):
        serial = get_object_or_404(Serial, pk=pk)
        episodes = serial.episode_set.all()
        return render(request, 'episodes.html', {'serial': serial, 'episodes': episodes})


class EpisodeView(View):

    def get(self, request, pk):
        episode = get_object_or_404(Episode, pk=pk)
        serial = episode.serial
        comments = Comment.objects.filter(page=request.path)
        is_watching = request.user.watching.filter(serial=serial.pk).count()
        return render(request, 'episode.html', {'serial': serial, 'episode': episode, 'comments': comments, 'is_watching': is_watching})

    def post(self, request, pk):
        if not request.user.pk:
            return HttpResponseRedirect('/login/')
        comment = Comment()
        comment.user_name = request.user.username
        comment.text = request.POST['text']
        comment.page = request.path
        comment.save()
        return self.get(request, pk)

    @staticmethod
    @login_required
    def check_as_watched(request, pk):
        episode = get_object_or_404(Episode, pk=pk)
        watching = get_object_or_404(SerialWatching, user=request.user.pk, serial=episode.serial.pk)
        watching.order = episode.order
        watching.save()
        return HttpResponseRedirect('/episode/' + pk + '/')


class MyEpisodesView(LoginRequiredMixin, View):

    def get(self, request):
        episodes = {}
        for watching in request.user.watching.all():
            serial = watching.serial
            episodes[serial] = serial.episode_set.filter(order__gt=watching.order)
        return render(request, 'my_episodes.html', {'dict': episodes})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class RegistrationView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "registration/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)


@permission_required('is_superuser')
def parse(request):
    serials.parser.pars_trakt_serials()
    return HttpResponseRedirect('/')


@permission_required('is_superuser')
def parse2(request):
    serials.parser.pars_watchseries_serials()
    return HttpResponseRedirect('/')