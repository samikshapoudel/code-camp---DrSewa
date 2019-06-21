from django import forms
from patient.models import Custom_patient, Make_appointment, Recharge_balance, CreateReport


class Custom_patient_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Custom_patient
        fields = ('username', 'email', 'password', 'gender', 'year', 'month', 'date', 'age')


class Make_appointment_form(forms.ModelForm):
    class Meta:
        model = Make_appointment
        fields = ('doctorEmailId', 'year', 'month', 'date', 'hr', 'min', 'problems')



class Recharge_form(forms.ModelForm):
    class Meta:
        model = Recharge_balance
        fields = '__all__'


class CreateReport_form(forms.ModelForm):
    class Meta:
        model = CreateReport
        fields = '__all__'

