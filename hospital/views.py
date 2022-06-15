from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from . import forms, models
from datetime import date

def home_view(request):
    # Checks if user that made request is authenticated, else, redirects to home page (index.html)
    if request.user.is_authenticated:
        return HttpResponseRedirect('after-login')
    
    return render(request, 'hospital/index.html')

# For showing signup / login button for Admin (by submit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after-login')
    
    return render(request, 'hospital/adminclick.html')

# For showing signup / login button for Doctor (by submit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after-login')
    
    return render(request, 'hospital/doctorclick.html')

# For showing signup / login button for patient (by submit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after-login')
    
    return render(request,'hospital/patientclick.html')

# Admin signup panel
def admin_signup_view(request):
    # Calls AdminSignupForm from forms.py
    form = forms.AdminSignupForm()
    # If we are sending the form then save new admin user
    if request.method == 'POST':
        form = forms.AdminSignupForm(request.POST)
        # Validates form
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            # Adds new admin user to 
            my_admin_group[0].user_set.add(user)
            
            # Redirects to Admin Login
            return HttpResponseRedirect('admin-login')
        
    return render(request,'hospital/adminsignup.html', {
        'form': form
        })

# Doctor signup panel
def doctor_signup_view(request):
    user_form = forms.DoctorUserForm()
    doctor_form = forms.DoctorForm()
    context_dict = {
        'userForm': user_form,
        'doctorForm': doctor_form
        }
    if request.method == 'POST':
        user_form = forms.DoctorUserForm(request.POST)
        doctor_form = forms.DoctorForm(request.POST, request.FILES)
        # Validates both forms
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            # Save Doctor User Form 
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

            # Redirects to Doctor Login
            return HttpResponseRedirect('doctor-login')
        
    return render(request, 'hospital/doctorsignup.html', context=context_dict)

# Patient signup panel
def patient_signup_view(request):
    user_form = forms.PatientUserForm()
    patient_form = forms.PatientForm()
    context_dict = {
        'userForm': user_form, 
        'patientForm': patient_form
        }
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST,request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            
        return HttpResponseRedirect('patient-login')
    return render(request,'hospital/patientsignup.html',context=context_dict)

# User type determination
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')


# Admin Views
# Admin Dashboard
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # Doctor and Patient List
    doctors = models.Doctor.objects.all().order_by('-id')
    patients = models.Patient.objects.all().order_by('-id')
    # Doctor, Patient, Appointment and Pending Approval Doctor, Patient, Appointment count
    doctor_count=models.Doctor.objects.all().filter(status=True).count()
    pending_doctor_count=models.Doctor.objects.all().filter(status=False).count()

    patient_count=models.Patient.objects.all().filter(status=True).count()
    pending_patient_count=models.Patient.objects.all().filter(status=False).count()

    appointment_count=models.Appointment.objects.all().filter(status=True).count()
    pending_appointment_count=models.Appointment.objects.all().filter(status=False).count()
    
    context_dict = {
    'doctors': doctors,
    'patients': patients,
    'doctorcount': doctor_count,
    'pendingdoctorcount': pending_doctor_count,
    'patientcount': patient_count,
    'pendingpatientcount': pending_patient_count,
    'appointmentcount': appointment_count,
    'pendingappointmentcount': pending_appointment_count,
    }
    
    return render(request, 'hospital/admin_dashboard.html', context=context_dict)

# Admin Sidebar Page
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, 'hospital/admin_doctor.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html', {'doctors': doctors})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    
    user_form = forms.DoctorUserForm(instance=user)
    doctor_form = forms.DoctorForm(request.FILES,instance=doctor)
    
    context_dict = {
        'userForm': user_form,
        'doctorForm': doctor_form
        }
    
    if request.method=='POST':
        user_form = forms.DoctorUserForm(request.POST, instance=user)
        doctor_form = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('admin-view-doctor')
        
    return render(request, 'hospital/admin_update_doctor.html', context=context_dict)

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    user_form=forms.DoctorUserForm()
    doctor_form=forms.DoctorForm()
    
    context_dict = {
        'userForm': user_form,
        'doctorForm': doctor_form
        }
    
    if request.method == 'POST':
        user_form = forms.DoctorUserForm(request.POST)
        doctor_form = forms.DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    
    return render(request,'hospital/admin_add_doctor.html',context=context_dict)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    # Doctor Approval
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, 'hospital/admin_approve_doctor.html', {'doctors':doctors})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_Specialisation.html', {'doctors':doctors})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, 'hospital/admin_patient.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_patient.html', {'patients': patients})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    user_form = forms.PatientUserForm(instance=user)
    patient_form = forms.PatientForm(request.FILES, instance=patient)
    
    context_dict = {
        'userForm': user_form,
        'patientForm': patient_form
        }
    
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST, instance=user)
        patient_form = forms.PatientForm(request.POST,request.FILES, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            patient = patient_form.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
        
    return render(request, 'hospital/admin_update_patient.html', context=context_dict)

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    user_form = forms.PatientUserForm()
    patient_form = forms.PatientForm()
    
    context_dict = {
        'userForm': user_form,
        'patientForm': patient_form
        }
    
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST,request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            
        return HttpResponseRedirect('admin-view-patient')
    
    return render(request,'hospital/admin_add_patient.html',context=context_dict)


# Approve Patient Admin
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    # Approval Needed
    patients = models.Patient.objects.all().filter(status=False)
    
    return render(request, 'hospital/admin_approve_patient.html', {'patients': patients})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    
    return redirect(reverse('admin-approve-patient'))

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    
    return redirect('admin-approve-patient')

# Discharging patient - Administration
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/admin_discharge_patient.html', {'patients': patients})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = (date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days # only how many day that is 2
    patient_dict = {
        'patientID': pk,
        'name': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }
    
    if request.method == 'POST':
        fee_dict ={
            'roomCharge': int(request.POST['roomCharge'])*int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patient_dict.update(fee_dict)
        
        # Updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientID = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST['medicineCost'])
        pDD.roomCharge = int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request, 'hospital/patient_final_bill.html', context=patient_dict)
    
    return render(request, 'hospital/patient_generate_bill.html', context=patient_dict)

# Discharge Patient Bill PDF
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download_pdf_view(request, pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientID=pk).order_by('-id')[:1]
    context_dict = {
        'patientName': dischargeDetails[0].patientName,
        'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
        'address': dischargeDetails[0].address,
        'mobile': dischargeDetails[0].mobile,
        'symptoms': dischargeDetails[0].symptoms,
        'admitDate': dischargeDetails[0].admitDate,
        'releaseDate': dischargeDetails[0].releaseDate,
        'daySpent': dischargeDetails[0].daySpent,
        'medicineCost': dischargeDetails[0].medicineCost,
        'roomCharge': dischargeDetails[0].roomCharge,
        'doctorFee': dischargeDetails[0].doctorFee,
        'OtherCharge': dischargeDetails[0].OtherCharge,
        'total': dischargeDetails[0].total,
    }
    
    return render_to_pdf('hospital/download_bill.html', context_dict)

# Appointment
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request, 'hospital/admin_appointment.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_appointment.html', {'appointments': appointments})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    
    context_dict = {
        'appointmentForm': appointmentForm,
        }
    
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorID = request.POST.get('doctorID')
            appointment.patientID = request.POST.get('patientID')
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorID')).first_name
            appointment.patientName = models.User.objects.get(id=request.POST.get('patientID')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    
    return render(request,'hospital/admin_add_appointment.html',context=context_dict)

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    # Approval
    appointments=models.Appointment.objects.all().filter(status=False)
    
    return render(request, 'hospital/admin_approve_appointment.html', {'appointments': appointments})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    
    return redirect(reverse('admin-approve-appointment'))

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

# Doctor Views
# Doctor Dashboard Views
@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    patient_count = models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointment_count = models.Appointment.objects.all().filter(status=True,doctorID=request.user.id).count()
    patient_discharged = models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    # Dashboard Table
    appointments = models.Appointment.objects.all().filter(status=True,doctorID=request.user.id).order_by('-id')
    patient_id = []
    
    for a in appointments:
        patient_id.append(a.patientID)
        
    patients = models.Patient.objects.all().filter(status=True,user_id__in=patient_id).order_by('-id')
    appointments = zip(appointments, patients)
    
    context_dict = {
    'patientcount': patient_count,
    'appointmentcount': appointment_count,
    'patientdischarged': patient_discharged,
    'appointments': appointments,
    'doctor': models.Doctor.objects.get(user_id=request.user.id), # For Doctor profile picture
    }
    
    return render(request, 'hospital/doctor_dashboard.html', context=context_dict)

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    context_dict = {
    'doctor':models.Doctor.objects.get(user_id=request.user.id), # For Doctor profile picture
    }
    
    return render(request, 'hospital/doctor_patient.html', context=context_dict)

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor = models.Doctor.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    return render(request, 'hospital/doctor_view_patient.html', {
        'patients': patients,
        'doctor': doctor
        })

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients = models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor = models.Doctor.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    return render(request, 'hospital/doctor_view_discharge_patient.html', {
        'dischargedpatients': dischargedpatients,
        'doctor': doctor
        })

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    return render(request, 'hospital/doctor_appointment.html', {'doctor':doctor})

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorID=request.user.id)
    patientid = []
    
    for a in appointments:
        patientid.append(a.patientID)
        
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{
        'appointments': appointments,
        'doctor': doctor
        })

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    appointments = models.Appointment.objects.all().filter(status=True,doctorID=request.user.id)
    patientid = []
    
    for a in appointments:
        patientid.append(a.patientID)
        
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments,patients)
    
    return render(request, 'hospital/doctor_delete_appointment.html',{
        'appointments': appointments,
        'doctor': doctor
        })

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    appointments = models.Appointment.objects.all().filter(status=True,doctorID=request.user.id)
    patientid = []
    
    for a in appointments:
        patientid.append(a.patientID)
        
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments,patients)
    
    return render(request, 'hospital/doctor_delete_appointment.html', {
        'appointments': appointments,
        'doctor': doctor
        })

# Patient Views
@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    
    context_dict = {
        'patient': patient,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
        }
    
    return render(request, 'hospital/patient_dashboard.html', context=context_dict)

@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    return render(request, 'hospital/patient_appointment.html', {'patient':patient})

@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(user_id=request.user.id) # Sidebar Doctor Profile Picture
    message = None
    
    context_dict = {
        'appointmentForm': appointmentForm,
        'patient': patient,
        'message': message
        }
    
    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            desc = request.POST.get('description')
            doctor = models.Doctor.objects.get(user_id=request.POST.get('doctorID'))
            
            if doctor.department == 'Cardiología':
                if 'corazón' in desc:
                    pass
                else:
                    message = 'Por favor escoge un doctor de acuerdo al departamento de tu caso'
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Dermatología':
                if 'piel' in desc:
                    pass
                else:
                    message = 'Por favor escoge un doctor de acuerdo al departamento de tu caso'
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Emergencias':
                pass

            if doctor.department == 'Alergias':
                if 'alergia' in desc:
                    pass
                else:
                    message = 'Por favor escoge un doctor de acuerdo al departamento de tu caso'
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'General':
                pass
            
            appointment = appointmentForm.save(commit=False)
            appointment.doctorID = request.POST.get('doctorID')
            appointment.patientID = request.user.id 
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorID')).first_name
            appointment.patientName = request.user.first_name 
            appointment.status=False
            appointment.save()            
        return HttpResponseRedirect('patient-view-appointment')
    
    return render(request,'hospital/patient_book_appointment.html',context=context_dict)

@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id) # Patient Sidebar Profile Picture
    appointments = models.Appointment.objects.all().filter(patientID=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{
        'appointments': appointments,
        'patient': patient
        })

@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id) # Patient Sidebar Profile Picture
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(patientID=patient.id).order_by('-id')[:1]
    patientDict = None
    if dischargeDetails:
        patientDict = {
            'is_discharged': True,
            'patient': patient,
            'patientID': patient.id,
            'patientName': patient.get_name,
            'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
            'address': patient.address,
            'mobile': patient.mobile,
            'symptoms': patient.symptoms,
            'admitDate': patient.admitDate,
            'releaseDate': dischargeDetails[0].releaseDate,
            'daySpent': dischargeDetails[0].daySpent,
            'medicineCost': dischargeDetails[0].medicineCost,
            'roomCharge': dischargeDetails[0].roomCharge,
            'doctorFee': dischargeDetails[0].doctorFee,
            'OtherCharge': dischargeDetails[0].OtherCharge,
            'total': dischargeDetails[0].total,
            }
    else:
        patientDict = {
            'is_discharged': False,
            'patient': patient,
            'patientID': request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


# About Us and Contact Us Views
def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(f'{name} || {email}', message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form': sub})