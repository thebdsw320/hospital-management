from django.db import models
from django.contrib.auth.models import User
from .utils import custom_id

DEPARTMENTS = [
    ('Cardiología','Cardiología'),
    ('Dermatología','Dermatología'),
    ('Emergencias','Emergencias'),
    ('Alergias','Alergias'),
    ('General','General'),
]

class Doctor(models.Model):
    id = models.CharField(primary_key=True, max_length=11, unique=True, default=custom_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/DoctorProfilePic/', 
        null=True, 
        blank=True
        )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, 
                                  choices=DEPARTMENTS, 
                                  default='General'
                                  )
    status = models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return f'{self.user.first_name} ({self.department})'

class Patient(models.Model):
    id = models.CharField(primary_key=True, max_length=11, unique=True, default=custom_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/',
                                    null=True,
                                    blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorId = models.PositiveIntegerField(null=False)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return f'{self.user.first_name} ({self.symptoms})'

class Appointment(models.Model):
    id = models.CharField(primary_key=True, max_length=11, unique=True, default=custom_id)
    patientID = models.CharField(max_length=11, null=True)
    doctorID = models.CharField(max_length=11, null=True)
    patientName = models.CharField(max_length=40,null=True)
    doctorName = models.CharField(max_length=40,null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

class PatientDischargeDetails(models.Model):
    # Patient Details
    patientID = models.CharField(max_length=11 ,null=True)
    patientName = models.CharField(max_length=40)
    assignedDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    # Dates Details
    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)

    # Charges Details
    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    otherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)