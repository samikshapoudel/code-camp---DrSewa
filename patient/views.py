from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from patient.forms import Custom_patient_form, Make_appointment_form, Recharge_form
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')


def patient_signup(request):
    if request.method == 'GET':
        custom_patient_form = Custom_patient_form()
        return render(request, 'patient_signup.html', {'form':custom_patient_form})
    else:
        user = Custom_patient_form(request.POST, request.FILES)
        if user.is_valid():
            user = user.save()
            user.set_password(user.password)
            user.save()
            user.is_staff =True
            user.is_superuser = True
            return HttpResponse ('You are registered')
        else:
            return HttpResponse('Error during submission')



def patient_login(request):
    if request.method == 'GET':
        custom_patient_form = Custom_patient_form()
        return render(request, 'patient_login.html', {'form':custom_patient_form})

    else:

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(username=username, password=password, email=email)


        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('patient_login')
            else:
                messages.warning(request, 'Sorry, You are not active.')
                return redirect('patient_signup')

        else:
            messages.error(request, 'Sorry Recheck your username or password')
            return redirect('patient_signup')


def patient_logout(request):
    logout(request)
    return redirect("patient_login")


