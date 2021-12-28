from django.contrib import admin

# Register your models here.
from .models import DoctorModel, Work
from .models import Patient, Doctor, Appointment, MedicalRecord, Prescription, Office

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)
admin.site.register(Office)

admin.site.register(DoctorModel)
admin.site.register(Work)