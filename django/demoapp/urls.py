from django.urls import path
from .views import index, submit, data_view

urlpatterns = [
    path('', index, name='index'),
    path('submit/', submit, name='submit'),
    path('data/', data_view, name='data'),
]
