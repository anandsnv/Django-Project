from django.contrib import admin
from facedectapi.models import User, Log

# Register your models here.
admin.site.register([User, Log])