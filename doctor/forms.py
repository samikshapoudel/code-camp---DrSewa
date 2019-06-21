from doctor.models import Custom_doctor, Validate_appointment, CreateDrReport
from django import forms

class Custom_doctor_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Custom_doctor
        fields = ('username', 'email', 'password', 'phone_no', 'gender', 'year', 'month', 'date', 'specialities', 'education'
                  , 'hospitals', 'rate')


class Validate_appointment_form(forms.ModelForm):
    class Meta:
        model = Validate_appointment
        fields = ('appointment_id', 'year', 'month', 'date', 'hr','min', 'changedatetime')


class CreateDrReport_form(forms.ModelForm):
    class Meta:
        model = CreateDrReport
        fields = '__all__'

