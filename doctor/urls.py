from django.urls import path
from doctor import views

urlpatterns = [
    path('', views.index, name = 'index'),

    path('doctor/', views.doctor, name = 'doctor'),
    path('patient/', views.patient, name='patient'),

    path('patient_signup/', views.patient_signup, name='patient_signup'),

    path('doctor_login/', views.doctor_login, name='doctor_login'),

    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),


    path('patient_login/', views.patient_login, name='patient_login'),

    path('makeappointment/', views.makeappointment, name = 'makeappointment'),
    path('doctors/', views.doctors, name = 'doctors'),
    path('validate_appointment/', views.validate, name = 'validate'),
    path('recharge/', views.recharge, name = 'recharge'),
    path('drreport/', views.drreport, name = 'drreport'),
    path('createreport/', views.createreport, name = 'createreport'),
    path('prescription/', views.prescription, name = 'prescription'),

]