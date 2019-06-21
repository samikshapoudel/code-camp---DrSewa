from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages


from doctor.forms import Custom_doctor_form, Validate_appointment

from django.contrib.auth import authenticate, login, logout

# Create your views here.

def doctor_signup(request):
    if request.method == 'GET':
        custom_doctor_form = Custom_doctor_form()
        return render(request, 'doctor_signup.html', {'form':custom_doctor_form})
    else:
        user = Custom_doctor_form(request.POST, request.FILES)
        if user.is_valid():
            user = user.save()
            user.set_password(user.password)
            user.save()
            user.is_staff =True
            user.is_superuser = True
            return HttpResponse ('You are registered')
        else:
            return HttpResponse('Error during submission')



def doctor_login(request):
    if request.method == 'GET':
        custom_doctor_form = Custom_doctor_form()
        return render(request, 'doctor_login.html', {'form':custom_doctor_form})

    else:

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(username=username, password=password, email=email)


        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('doctor_login')
            else:
                messages.warning(request, 'Sorry, You are not active.')
                return redirect('doctor_signup')

        else:
            messages.error(request, 'Sorry Recheck your username or password')
            return redirect('doctor_signup')


def doctor_logout(request):
    logout(request)
    return redirect("doctor_login")





