from patient import views
from django.urls import path


urlpatterns = [
    path('', views.index),
    path('index/', views.index, name = 'index'),
    path('patient_signup/', views.patient_signup, name='signup'),
    path('patient_login/', views.patient_login, name='login'),

]
