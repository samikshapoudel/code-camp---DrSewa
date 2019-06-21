from django.urls import path
from doctor import views

urlpatterns = [
path('doctor_signup/', views.doctor_signup, name='login'),
path('doctor_login/', views.doctor_login, name='login'),
]