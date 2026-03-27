from django.urls import path
from .views import template_create, template_detail, template_list, template_version_create

urlpatterns = [
    path('', template_list, name='template_list'),
    path('new/', template_create, name='template_create'),
    path('<int:pk>/', template_detail, name='template_detail'),
    path('<int:pk>/versions/new/', template_version_create, name='template_version_create'),
]
