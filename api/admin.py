from django.contrib import admin
from .models import *

admin.site.register(Company)
admin.site.register(HR)
admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(Skill)
admin.site.register(Experience)