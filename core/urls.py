from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', include('sim.urls')),   # Include all URLs from sim app
]
