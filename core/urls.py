from django.urls import path,re_path
from .views import *

app_name = 'core'


urlpatterns = [
    path('',home,name='home'),
    path('404', notfound, name='404'),
    path('contact',contact,name='contact'),
    path('info',info,name='info'),
    path('signin',signin,name='signin'),
    path('logout/', logout_user,name='logout'),
    path('service/<slug:category>', service, name='service'),
    path('pay/<uuid:prodid>/', payment, name='pay'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
    activate, name='activate'),
]



