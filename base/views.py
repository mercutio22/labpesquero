# Create your views here.

from django.views.generic import DetailView
from base.models import Laudo

class LaudoDetail(DetailView):
    model=Laudo
    template_name='base/report.html'

