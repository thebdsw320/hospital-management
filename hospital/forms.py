from django import forms
from django.contrib.auth.models import User
from . import models

# Administration Sign Up Form 
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

# Doctor Sign Up Form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
# Doctor Details Form
class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['address','mobile','department','status','profile_pic']

# Patient Sign Up Form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

# Patient Details Form
class PatientForm(forms.ModelForm):
    # Link Patient with assigned Doctor
    assignedDoctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label='Name and Department', to_field_name='user_id')
    class Meta:
        model = models.Patient
        fields = ['address','mobile','status','symptoms','profile_pic']

# Appointment Form
class AppointmentForm(forms.ModelForm):
    doctorID = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label='Doctor Name and Department', to_field_name='user_id')
    patientID = forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label='Patient Name and Symptoms', to_field_name='user_id')
    class Meta:
        model=models.Appointment
        fields=['description','status']

# Appointment for Patient Form
class PatientAppointmentForm(forms.ModelForm):
    doctorID = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label='Doctor Name and Department', to_field_name='user_id')
    class Meta:
        model = models.Appointment
        fields = ['description','status']

# Contact Us Form
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(
            attrs={
                'rows': 3, 
                'cols': 30
                }
            ))