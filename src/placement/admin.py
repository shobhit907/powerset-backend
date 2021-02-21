from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Company)
admin.site.register(Coordinator)
admin.site.register(Placement)
admin.site.register(JobProfile)
admin.site.register(JobApplicant)
admin.site.register(JobRound)