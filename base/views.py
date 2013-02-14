# Create your views here.

from django_xhtml2pdf.utils import generate_pdf
from django.http import HttpResponse

def createPDF(response):
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('base/report.html', file_object=resp)
    return result
