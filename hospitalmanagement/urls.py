from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView

# TO-DO Describe all URL Paths

# Administration URLs
urlpatterns = [
    # Admin Site
    path('admin/', admin.site.urls),
    # Home
    path('', views.home_view, name=''),
    # About Us
    path('about-us', views.aboutus_view),
    # Contact Us
    path('contact-us', views.contactus_view),
    # Admin Auth for showing signup/login button 
    path('admin-auth', views.adminclick_view),
    # Doctor Auth for showing signup/login button 
    path('doctor-auth', views.doctorclick_view),
    # Patient Auth for showing signup/login button 
    path('patient-auth', views.patientclick_view),
    # Register new Admin User
    path('admin-signup', views.admin_signup_view),
    # Register new Doctor User
    path('doctor-signup', views.doctor_signup_view,name='doctorsignup'),
    # Register new Patient User
    path('patient-signup', views.patient_signup_view),
    # Login as Admin User
    path('admin-login', LoginView.as_view(template_name='hospital/adminlogin.html')),
    # Login as Doctor User
    path('doctor-login', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    # Login as Patient User
    path('patient-login', LoginView.as_view(template_name='hospital/patientlogin.html')),
    # Afer entering credentials, checks whether username and password is part of admin user, doctor user or patient user
    path('after-login', views.afterlogin_view, name='after-login'),
    # Logout
    path('logout', LogoutView.as_view(template_name='hospital/index.html'), name='logout'),
    # Admin Dashboard
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<str:pk>', views.delete_doctor_from_hospital_view, name='delete-doctor-from-hospital'),
    path('update-doctor/<str:pk>', views.update_doctor_view, name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view, name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('approve-doctor/<str:pk>', views.approve_doctor_view, name='approve-doctor'),
    path('reject-doctor/<str:pk>', views.reject_doctor_view, name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view, name='admin-view-doctor-specialisation'),
    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<str:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<str:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<str:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<str:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<str:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<str:pk>', views.download_pdf_view,name='download-pdf'),
    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<str:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<str:pk>', views.reject_appointment_view,name='reject-appointment'),
]

# Doctors URLs
urlpatterns += [
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<str:pk>', views.delete_appointment_view,name='delete-appointment'),
]

# Patients URLs
urlpatterns += [
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),
]