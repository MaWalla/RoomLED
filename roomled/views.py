from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView

from .forms import MainForm


class MainView(LoginRequiredMixin, FormView):
    template_name = 'roomled/index.html'
    form_class = MainForm

    def form_valid(self, form):
        return HttpResponse(status=200)

    def form_invalid(self, form):
        return HttpResponse(status=400)


class CheatSheetView(TemplateView):
    template_name = 'roomled/cheat-sheet.html'
