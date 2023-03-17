from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from crm import models


admin.site.register(get_user_model(), ModelAdmin)

admin.site.register(models.Customer)

admin.site.register(models.Contract)
admin.site.register(models.ContractStatus)

admin.site.register(models.Event)
admin.site.register(models.EventStatus)
