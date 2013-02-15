from django.conf.urls import patterns, include, url
from wkhtmltopdf.views import PDFTemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import (TemplateView,
                                  )
from base.models import Laudo
from base.views import LaudoDetail
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labpesquero.views.home', name='home'),
    url(r'^referencias', include('publications.urls')),
    
    #the grappelli admin skin
    url(r'^grappelli/', include('grappelli.urls')),
    
    #the bibtex import view must precede the admin site url patterns
    url(r'^admin/publications/publication/import_bibtex/$',
        'publications.admin_views.import_bibtex'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^laudo/$', TemplateView.as_view(template_name='base/report.html'),
        name='laudo_detail'),

    url(r'^laudopdf/$', 'base.views.createPDF', name='criaPDF'),
    url(r'^laudopdfwk/$',
        PDFTemplateView.as_view(template_name='base/report.html'),
        name='webkitPDF'),
    url(r'^laudo/(?P<pk>\d+)/$', LaudoDetail.as_view(),
        name='laudo-detalhe'),
)
