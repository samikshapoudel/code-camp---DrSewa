from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView
from doctor.models import Patient, Doctor, Make_appointment, Validate_appointment, Recharge_balance, CreateReport, CreateDrReport
from doctor.forms import PatientSignUpForm, DoctorSignUpForm, Validate_appointment_form, Recharge_form, Prescription_form, Make_appointment_form, CreateDrReport_form, CreateReport_form
from django.contrib.auth.decorators import login_required
import requests
import json
import datetime
import re

logged_user = {}


from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, 'index.html')


def doctor(request):
    return render(request, 'doctor.html')

def patient(request):
    return render(request, 'patient.html')


def doctor_signup(request):
    if request.method == 'GET':
        custom_doctor_form = DoctorSignUpForm()
        return render(request, 'doctor_signup.html', {'form':custom_doctor_form})
    else:
        doc_dict = {
            "$class": "com.pax.drsewa.CreateDoctor",
            "emailId": "string",
            "name": "string",
            "year": 0,
            "month": 0,
            "date": 0,
            "gender": "MALE",
            "specialities": [],
            "education": [],
            "description": "string",
            "hospitals": [],
            "rate": 0
        }

        user = Doctor(request.POST)
        doc_dict['name'] = request.POST['username']
        doc_dict['emailId'] = request.POST['email']
        dob = request.POST['dob']
        dob = dob.split('-')
        doc_dict['year'] = dob[0]
        doc_dict['month'] = dob[1]
        doc_dict['date'] = dob[2]
        doc_dict['gender'] = request.POST['gender']
        specialities = request.POST['specialities']
        specialities = specialities.split(",")
        specialities_list = [i.lstrip() for i in specialities]
        doc_dict['specialities'] = specialities_list
        education = request.POST['education']
        education = education.split(',')
        education_list = [i.lstrip() for i in education]
        doc_dict['education'] = education_list
        doc_dict['description'] = request.POST['description']
        hospitals = request.POST['hospitals']
        hospitals = hospitals.split(',')
        hospitals_list = [i.lstrip() for i in hospitals]
        doc_dict['hospitals'] = hospitals_list
        doc_dict['rate'] = request.POST['rate']

        doc_dict_json = json.dumps(doc_dict)

        print(doc_dict_json)

        output = requests.post('http://localhost:3000/api/CreateDoctor', headers={"content-type": "application/json"}   , data=doc_dict_json)
        if (output.status_code == 200):
            #return HttpResponse(output.text+"<br><br><br>"+doc_dict_json)
            return redirect('doctor_login')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+doc_dict_json+"<br><br><br>"+"json: "+ str(output.status_code))

def doctor_login(request):
    if request.method == 'GET':
        print('cookie: ',   request.COOKIES.get('id'))
        custom_doctor_form = DoctorSignUpForm()
        return render(request, 'doctor_login.html', {'form':custom_doctor_form})
    elif request.method == 'POST':
        port = request.POST['port']
        email = request.POST['email']
        #response = HttpResponse('''You have logged in<br><a href="{% url 'doctorview' %}">Redirect</a>''')
        response = redirect("doctorview")
        response.set_cookie('id', port)
        response.set_cookie('email', email)
        response.set_cookie("category", 'Doctor')
        return response

    else:

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(username=username, password=password, email=email)


        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('doctorpage')
            else:
                messages.warning(request, 'Sorry, You are not active.')
                return redirect('doctor_signup')

        else:
            messages.error(request, 'Sorry Recheck your username or password')
            return redirect('doctor_login')


def doctor_logout(request):
    logout(request)
    return redirect("doctor_login")


def patient_signup(request):
    if request.method == 'GET':
        custom_patient_form = PatientSignUpForm()
        return render(request, 'patient_signup.html', {'form':custom_patient_form})
    else:
        patient_dict = {
                "$class": "com.pax.drsewa.CreatePatient",
                "emailId": "string",
                "name": "string",
                "year": 0,
                "month": 0,
                "date": 0,
                "gender": "MALE"
        }

        user = Patient(request.POST, request.FILES)
        patient_dict['name'] = request.POST['username']
        patient_dict['emailId'] = request.POST['email']
        dob = request.POST['dob']
        dob = dob.split('-')
        patient_dict['year'] = dob[0]
        patient_dict['month'] = dob[1]
        patient_dict['date'] = dob[2]
        patient_dict['gender'] = request.POST['gender']

        patient_dict_json = json.dumps(patient_dict)

        output = requests.post('http://localhost:3000/api/CreatePatient', headers={"content-type": "application/json"}, data=patient_dict_json)
        if (output.status_code == 200):
            return redirect('patient_login')
        else:
            print(output.json)
            return HttpResponse(
                'Something Error: <br>' + output.text + "<br><br><br>" + patient_dict_json + "<br><br><br>" + "json: " + str(
                    output.status_code))


def patient_login(request):
    if request.method == 'GET':
        custom_patient_form = PatientSignUpForm()
        return render(request, 'patient_login.html', {'form':custom_patient_form})
    elif request.method == 'POST':
        port = request.POST['port']
        email = request.POST['email']
        #response = HttpResponse('''You have logged in<br><a href="{% url 'patientview' %}">Redirect</a>''')
        response = redirect('patientview')
        response.set_cookie('id', port)
        response.set_cookie('email', email)
        response.set_cookie('category', 'Patient')
        return response
    else:

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        port = request.POST.get('port')

       # output = requests.get('http://localhost:3000/api/Doctor', headers={"content-type": "application/json",})
        # user = authenticate(username=username, password=password, email=email)

        # if user:
        #     if user.is_active:
        #         login(request, user)
        #         messages.success(request, 'Login Successful')
        #         return redirect('patient_login')
        #     else:
        #         messages.warning(request, 'Sorry, You are not active.')
        #         return redirect('patient_signup')

        # else:
        #     messages.error(request, 'Sorry Recheck your username or password')
        #     return redirect('patient_signup')


def user_logout(request):
    response = redirect('patient_login')
    if request.COOKIES.get('category') == "Doctor":
        response = redirect('doctor_login')
    response.delete_cookie('email')
    response.delete_cookie('category')
    return response   



#@login_required(login_url='index.html')
def makeappointment(request):
    if request.method == 'GET':
        appointment = Make_appointment_form()
        is_mobile = mobile(request)
        return render(request, 'makeappointment.html', {'form':appointment, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}, "is_mobile":is_mobile})

    else:
        appointment_form = Make_appointment_form(request.POST)
        data = {
        "$class": "com.pax.drsewa.MakeAppointment",
        "doctorEmailId": "string",
        "year": 0,
        "month": 0,
        "date": 0,
        "hr": 0,
        "min": 0,
        "problems": []
        }
        data['doctorEmailId'] = request.POST['doctorEmailId']
        dob = request.POST['dob']
        dob = dob.split('-')
        data['year'] = dob[0]
        data['month'] = dob[1]
        data['date'] = dob[2]
        time = request.POST['time']
        time = time.split(':')
        data['hr'] = time[0]
        data['min'] = time[1]
        problems = request.POST['problems']
        problems = problems.split(",")
        problems = [i.lstrip() for i in problems]
        data['problems'] = problems

        data_json = json.dumps(data)
        
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/MakeAppointment', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            #return HttpResponse("Successfully applied appointment<br><br><br>"+output.text+"<br><br><br>")
            return redirect('viewappointment')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))

        # if appointment_form.is_valid():

        #     return HttpResponse('Submitted')
        # else:
        #     return HttpResponse('Not Submitted')

def viewappointment(request):
    output = requests.get('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/Appointment')
    o = json.loads(output.text)
    # for i in o:
    #     i['patient'] = i.split('#')[1]
    #     i['doctor'] = i.split('#')[1]
    n = datetime.datetime.now()
    nowdatetime = {"year":n.date().year, "month":n.date().month, "date":n.date().day, "hour":n.time().hour, "minute":n.time().minute}
    print(nowdatetime)
    o = {"data":o, "nowdatetime":nowdatetime, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}}
    return render(request, 'appointment_view.html', o)

def doctors(request):
    doctors = Doctor.username
    return render(request, 'doctors.html', context={'doctors': doctors,"who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})

def validate(request):
    if request.method=='GET':
        validate = Validate_appointment_form()
        return render(request, 'validateAppointment.html', {"form": validate, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})
    else:
        data = {
        "$class": "com.pax.drsewa.ValidateAppointment",
        "appointmentId": "string",
        "year": 0,
        "month": 0,
        "date": 0,
        "hr": 0,
        "min": 0,
        "changeDateTime": "false"
        }
        data['appointmentId'] = request.POST['appointment_id']
        if request.POST['changedatetime'] == "YES" or request.POST['changedatetime'] == "yes" or request.POST['changedatetime'] == "Y" or request.POST['changedatetime'] == "y":
            data['changeDateTime'] = "true"
            dob = request.POST['dob']
            dob = dob.split('-')
            data['year'] = dob[0]
            data['month'] = dob[1]
            data['date'] = dob[2]
            time = request.POST['time']
            time = time.split(':')
            data['hr'] = time[0]
            data['min'] = time[1]

        data_json = json.dumps(data)
        
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/ValidateAppointment', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            #return HttpResponse("Successfully validated appointment<br><br><br>"+output.text+"<br><br><br>")
            return redirect('viewappointment')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))

        

def createreport(request):
    if request.method == 'GET':
        report = CreateReport_form()
        return render(request, 'createreport.html', {'form':report, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})

    else:
        report_form = CreateReport_form(request.POST)

        data = {
        "$class": "com.pax.drsewa.CreateReport",
        "year": 0,
        "month": 0,
        "date": 0,
        "content": [],
        "institute": "string"
        }
        dob = request.POST['dob']
        dob = dob.split('-')
        data['year'] = dob[0]
        data['month'] = dob[1]
        data['date'] = dob[2]
        content = request.POST['content']
        content = content.split(',')
        data['content'] = content
        data['institute'] = request.POST['institute']
        
        data_json = json.dumps(data)
        
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/CreateReport', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            #return HttpResponse("Successfully created report<br><br><br>"+output.text+"<br><br><br>")
            return redirect('drreport')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))



def createreportDr(request):
    if request.method == 'GET':
        report = CreateReport_form()
        return render(request, 'createreportDr.html', {'form':report, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})

    else:
        report_form = CreateReport_form(request.POST)

        data = {
        "$class": "com.pax.drsewa.CreateReportDr",
        "year": 0,
        "month": 0,
        "date": 0,
        "content": [],
        "institute": "string",
        "patient": "string"
        }
        dob = request.POST['dob']
        dob = dob.split('-')
        data['year'] = dob[0]
        data['month'] = dob[1]
        data['date'] = dob[2]
        content = request.POST['content']
        content = content.split(',')
        data['content'] = content
        data['institute'] = request.POST['institute']
        data['patient'] = request.POST['patient']
        
        data_json = json.dumps(data)
        
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/CreateReportDr', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            return redirect('drreport')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))


def drreport(request):
    if request.method == 'GET':
        output = requests.get('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/Report')
        o = json.loads(output.text)
        # for i in o:
        #     i['patient'] = i.split('#')[1]
        #     i['doctor'] = i.split('#')[1]
        o = {"data":o, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}}
        return render(request, 'report_view.html', o)
        # report = CreateDrReport_form()
        # return render(request, 'report_view.html', {'form':report})

    else:
        report_form = CreateDrReport_form(request.POST)
        if report_form.is_valid():
            return HttpResponse('Submitted')
        else:
            return HttpResponse('Not Submitted')


def recharge(request):
    if request.method == 'GET':
        card = Recharge_form()
        return render(request, 'recharge.html', {'form':card, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})

    else:
        rechargepin = request.POST['recharge']
        data = {
        "$class": "com.pax.drsewa.RechargeBalance",
        "rechargeCard": 0
        }
        data['rechargeCard'] = rechargepin
        data_json = json.dumps(data)
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/RechargeBalance', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            return redirect('patientview')
        else:
            return HttpResponse('<h2>Recharge Invalid</h2> <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))
        # if card.is_valid():
        #     card.recharge_card+=card
        #     return HttpResponse('Balance added successfully')

        # else:
        #     return HttpResponse('Please enter valid amount')


def prescription(request):
    if request.method == 'GET':
        prescription = Prescription_form()
        return render(request, 'prescription.html', {'form': prescription, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})

    else:
        data = {
        "$class": "com.pax.drsewa.CreatePrescription",
        "diagnosis": "string",
        "medications": [],
        "patient": "string"
        }
        data['diagnosis'] = request.POST['diagnosis']
        medications = request.POST['medications']
        medications = medications.split(',')
        medications = [i.lstrip() for i in medications]
        data['medications'] = medications
        data['patient'] = request.POST['patient']

        data_json = json.dumps(data)
        
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/CreatePrescription', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            #return HttpResponse("Successfully created Prescription<br><br><br>"+output.text+"<br><br><br>")
            return redirect('viewprescription')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))



        # prescription = Prescription_form(request.POST)
        # if prescription.is_valid():
        #     prescription.save()
        #     return HttpResponse('Saved successfully!')



def doctorpage(request):
    if request.method == 'GET':
        patient = PatientSignUpForm()
        appointment = Make_appointment_form()
        report = CreateReport_form()
        prescription = Prescription_form()
        return render(request, 'doctorpage.html', {'patient':patient, 'appointment':appointment, 'report':report,
'prescription':prescription, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})


def prescription_view(request):
    output = requests.get('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/Prescription')
    o = json.loads(output.text)
    # for i in o:
    #     i['patient'] = i.split('#')[1]
    #     i['doctor'] = i.split('#')[1]
    o = {"data":o, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}}
    return render(request, 'prescription_view.html', o)


def doctor_view(request):
    if request.method == 'GET':
        output = requests.get('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/Doctor')
        o = json.loads(output.text)
        o.sort(key = lambda x: x['rating'], reverse=True)
        o = {"doctors":o, "searchvalue":"search by specialities", "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}}
        return render(request, 'doctors.html', o)
    elif request.method == 'POST':
        output = requests.get('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/Doctor')
        o = json.loads(output.text)
        o.sort(key = lambda x: x['rating'], reverse = True)
        l = []
        searchkey = request.POST['searchkey']
        for i in o:
            if re.search(searchkey, str(i['specialities']), flags=re.IGNORECASE):
                l.append(i)
        o = {"doctors":l, "searchvalue":searchkey, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}}
        return render(request, 'doctors.html', o)


def patient_view(request):
    output = requests.get('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/Patient')
    o = json.loads(output.text)
    o = {"patients":o, "who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}}
    return render(request, 'patients.html', o)

       
def rating_doctor(request):
    if request.method=='GET':
        return render(request, 'ratingDoctor.html', {"who":{"email": request.COOKIES.get('email'), "category": request.COOKIES.get("category")}})
    else:
        data = {
        "$class": "com.pax.drsewa.RateDoctor",
        "emailId": "string",
        "rating": 0
        }
        data['emailId'] = request.POST['email']
        rating = request.POST['rating']
        if int(rating)>5:
            rating = 5
        elif int(rating)<0:
            rating = 0
        data['rating'] = str(rating)
        data_json = json.dumps(data)
        
        output = requests.post('http://127.0.0.1:'+request.COOKIES.get('id')+'/api/RateDoctor', headers={"content-type": "application/json"}, data=data_json)

        if (output.status_code == 200):
            #return HttpResponse("Successfully validated appointment<br><br><br>"+output.text+"<br><br><br>")
            return redirect('doctorview')
        else:
            print(output.json)
            return HttpResponse('Something Error: <br>'+ output.text+"<br><br><br>"+"<br><br><br>"+"json: "+ str(output.status_code))




def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False