from django.urls import path
from BlogWebsite.account.views import registration_view

urlpatterns = (
    path('register/', registration_view, name='register'),
)
