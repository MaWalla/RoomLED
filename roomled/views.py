import socket
import threading

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from roomled.models import Device
from roomled.utils.nodemcu_handler import send_request, send_data
from .forms import MainForm


class BaseMainView(FormView):
    template_name = 'roomled/index.html'
    form_class = MainForm
    form_url = reverse_lazy('main')

    def __init__(self):
        self.devices = Device.objects.all()
        super().__init__()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            devices=self.devices,
            form_url=self.form_url,
            **kwargs,
        )

    def form_valid(self, form):
        send_data(form.cleaned_data, Device.objects.all())
        return HttpResponse(status=200)

    def form_invalid(self, form):
        return HttpResponse(status=400)


class GeoFenceView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('token') == settings.API_TOKEN:
            in_zone = self.clean_inzone(request.GET.get('inzone'))
            devices = Device.objects.all()
            mode = {f'device-{device.id}': 'on' for device in devices}

            if in_zone:
                mode['mode'] = 'random'
            else:
                mode['mode'] = 'off'
            send_data(mode, devices)

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)

    @staticmethod
    def clean_inzone(inzone):
        if str(inzone).lower() == 'true':
            return True
        elif str(inzone).lower() == 'false':
            return False
        else:
            return None


class MainView(LoginRequiredMixin, BaseMainView):
    pass


class UserLoginView(LoginView):
    template_name = 'roomled/login.html'

    def get_success_url(self):
        return reverse('main')


class UserLogoutView(LogoutView):
    next_page = 'login'


class GuestView(BaseMainView):
    form_url = reverse_lazy('guest')

    def dispatch(self, request, *args, **kwargs):
        host, port = request.META.get('HTTP_HOST').split(':')
        host_ip = socket.gethostbyname(host)
        client = request.META.get('REMOTE_ADDR')
        if '192.168.' in client or host_ip == client:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('not-guest')


class NotGuestView(TemplateView):
    template_name = 'roomled/not-guest.html'
