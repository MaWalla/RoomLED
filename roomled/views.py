import threading

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView

from roomled.models import Device
from roomled.utils.nodemcu_handler import send_request
from .forms import MainForm


class MainView(LoginRequiredMixin, FormView):
    template_name = 'roomled/index.html'
    form_class = MainForm

    def __init__(self):
        self.devices = Device.objects.all()
        super().__init__()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            devices=self.devices,
            **kwargs,
        )

    def form_valid(self, form):
        self.send_data(form.cleaned_data)
        return HttpResponse(status=200)

    def form_invalid(self, form):
        return HttpResponse(status=400)

    def send_data(self, data):
        mode = self.get_mode(data)

        for device in self.devices:
            threading.Thread(target=send_request, args=(device, mode), kwargs={}).start()

    @staticmethod
    def get_mode(data):
        mode_name = data.get('mode')
        mode = {}

        if mode_name in ['single_color', 'random_lead_color']:
            mode = {
                mode_name: {'input_color': data.get('color1')}
            }
        elif mode_name in ['gradient', 'random_lead_gradient']:
            mode = {
                mode_name: {'input_color1': data.get('color1'), 'input_color2': data.get('color2')}
            }
        elif mode_name in {'off', 'random'}:
            mode = {
                mode_name: None
            }

        return mode


class CheatSheetView(TemplateView):
    template_name = 'roomled/cheat-sheet.html'
