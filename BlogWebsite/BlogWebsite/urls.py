from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", include('BlogWebsite.personal.urls')),
    path("account/", include('BlogWebsite.account.urls')),
]
