from django.urls import path
from .views import personnel_create, personnel_detail, personnel_list

urlpatterns = [
    path('personnel/', personnel_list, name='personnel_list'),
    path('personnel/new/', personnel_create, name='personnel_create'),
    path('personnel/<int:pk>/', personnel_detail, name='personnel_detail'),
]
