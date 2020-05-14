from django.urls import path, include

from . import views

urlpatterns = [
    path('v1/', include([
        path('auth/', include('rest_auth.urls')),
    ]))
]