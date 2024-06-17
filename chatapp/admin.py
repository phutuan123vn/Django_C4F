from django.contrib import admin
import chatapp.models as models
# Register your models here.
admin.site.register(models.Message)
admin.site.register(models.Code)
admin.site.register(models.Room)