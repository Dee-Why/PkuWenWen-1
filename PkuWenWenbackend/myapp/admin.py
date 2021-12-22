from django.contrib import admin

# Register your models here.
from .models import Office, DoctorModel, Work

admin.site.register(Office)
admin.site.register(DoctorModel)
admin.site.register(Work)