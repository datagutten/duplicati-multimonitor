from django.contrib import admin
from django.urls import path, include

from monitoring import views

app_name = 'monitoring'
urlpatterns = [
    # path('report', views.report, name='report'),
    path('', views.jobs, name='status'),
    path('', views.jobs, name='index'),
    path('run', views.run_log, name='run'),
    path('run/<int:run>', views.run_log, name='run'),
    path('runs', views.runs, name='runs'),
    path('jobs', views.jobs, name='jobs'),
    path('status', views.status_matrix, name='status_matrix'),
    path('ajax/', include('monitoring.urls_ajax')),
    path('host/<str:host>', views.host_info, name='host'),
    path('job/<int:job>', views.job_info, name='job')
]
