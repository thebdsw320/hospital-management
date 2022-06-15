from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails

# Doctor Administration Model - Inherited from Doctor model 
class DoctorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Doctor, DoctorAdmin)

# Patient Administration Model - Inherited from Patient model
class PatientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Patient, PatientAdmin)

# Appointment Administration Model - Inherited from Appointment model
class AppointmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Appointment, AppointmentAdmin)

# Patient Discharge Details Administration Model - Inherited from PatientDischargeDetails
class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)