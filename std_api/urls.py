
from django.contrib import admin
from std_api import state
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
     path('state/', state.state),
]
