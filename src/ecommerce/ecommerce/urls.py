"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from billing.views import payment_method_view,payment_method_create_view
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.views import LogoutView
from carts.views import cart_detail_api_view
from orders.views import LibraryView
from marketing.views import MarketingPreferenceUpdateView,MailchimpWebhookView
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from accounts.views import LoginView,RegistrationView,GuestRegisterView
from .views import home_page,about_page,contact_page
#from products.views import (ProductListView,
                            #ProductDetailView,
                            #product_detail_view,
                            #product_list_view,
                            #ProductFeaturedListView,
                            #ProductDetailSlugView,
                            #ProductFeaturedDetailView)


urlpatterns = [
    url(r'^$',home_page,name='home'),
    url(r'^about/$',about_page,name='about'),
   # url(r'^account/login/$',RedirectView.as_view(url='/login')),
    url(r'^accounts/$',RedirectView.as_view(url='/account')),
    url(r'^settings/$',RedirectView.as_view(url='/account')),
    url(r'^contact/$',contact_page,name='contact'),
    url(r'^register/$',RegistrationView.as_view(),name='register'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^api/cart/$',cart_detail_api_view,name='api-cart'),
    url(r'^billing/payment-method/$',payment_method_view,name='billing-payment-method'),
    url(r'^register/guest/$',GuestRegisterView.as_view(),name='guest_register'),
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),
    url(r'^settings/email/$',MarketingPreferenceUpdateView.as_view(),name='marketing-pref'),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    url(r'^billing/payment-method/create/$',payment_method_create_view,name='billing-payment-method-endpoint'),
    url(r'^bootstrap/$',TemplateView.as_view(template_name="bootstrap/example.html")),
    url(r'^library/$',LibraryView.as_view(),name="library"),
    
    url(r'^products/',include("products.urls",namespace="products")),
    url(r'^search/',include("search.urls",namespace="search")),
    url(r'^cart/',include("carts.urls",namespace='cart')),
    url(r'^account/', include("accounts.urls", namespace='account')),
    url(r'^orders/', include("orders.urls", namespace='orders')),
    
    url(r'^accounts/',include("accounts.passwords.urls")),
    url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 #url(r'^products/$',ProductListView.as_view()),
    #url(r'^products-fbv/$',product_list_view),
    #url(r'^featured/$',ProductFeaturedListView.as_view()),
    #url(r'^featured/(?P<pk>\d+)/$',ProductFeaturedDetailView.as_view()),
    #url(r'^products/(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view()),
    #url(r'^products/(?P<pk>\d+)/$',ProductDetailView.as_view()),
    #url(r'^products-fbv/(?P<pk>\d+)/$',product_detail_view),
       