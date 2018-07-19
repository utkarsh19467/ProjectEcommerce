
from django.conf.urls import url
from .views import (AccountHomeView,AccountEmailActivationView,UserDetailUpdateView)
from products.views import UserProductHistoryView                            


urlpatterns = [
    url(r'^$',AccountHomeView.as_view(),name='home'),
    url(r'^details/$',UserDetailUpdateView.as_view(),name='user-update'),
    url(r'^history/products/$',UserProductHistoryView.as_view(),name='history-product'),
    
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivationView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/$', AccountEmailActivationView.as_view(), name='resend-activation'),
]

