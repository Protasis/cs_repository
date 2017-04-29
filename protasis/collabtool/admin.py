from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.Institution)
admin.site.register(models.Project)
admin.site.register(models.Venue)
admin.site.register(models.InstitutionAuthor)
