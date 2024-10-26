from django.contrib import admin
from django.urls import path, include

from monitoring.views import ajax as views

app_name = 'mon_ajax'
urlpatterns = [
    path('backup_size/<int:job>', views.backup_size, name='backup_size')
]
