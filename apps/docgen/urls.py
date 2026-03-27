from django.urls import path
from .views import generate_personnel_form

urlpatterns = [
    path('personnel/<int:pk>/generate/', generate_personnel_form, name='generate_personnel_form'),
]
