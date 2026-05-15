from django.urls import path
from . import views

urlpatterns = [
    path('', views.family_portal, name='family_portal'),
    path('timeline/', views.family_timeline, name='family_timeline'),
]