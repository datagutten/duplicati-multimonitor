from django.urls import path

from duplicati import views

app_name = 'duplicati'
urlpatterns = [
    path('report/<str:key>', views.report, name='report'),
]
