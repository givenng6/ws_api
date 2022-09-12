
from django.contrib import admin
from std_api import state
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('state/', state.state),
    path("auth/", include('authentication.urls')),
    path("db/", include('database.urls')),
]
