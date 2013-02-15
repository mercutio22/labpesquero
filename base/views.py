# Create your views here.

from django_xhtml2pdf.utils import generate_pdf
from django.http import HttpResponse
from django.views.generic import DetailView
from base.models import Laudo

def createPDF(response):
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('base/report.html', file_object=resp)
    return result

class LaudoDetail(DetailView):
    model=Laudo
    template_name='base/report.html'

