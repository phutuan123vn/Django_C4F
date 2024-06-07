from django.contrib import admin
from blog import models

# Register your models here.
admin.site.register(models.Blog)
admin.site.register(models.BlogComment)
admin.site.register(models.BlogLike)
