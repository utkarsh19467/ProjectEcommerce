
from django.conf.urls import url
from django.contrib import admin
from products.views import (ProductListView,
                            ProductDownloadView,
                            ProductDetailSlugView)
                            


urlpatterns = [
    url(r'^$',ProductListView.as_view(),name='list'),
    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(),name='detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$',ProductDownloadView.as_view(),name='download'),
    
    
]

