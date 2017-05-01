from django.contrib import admin
from .models import Author, Institution, InstitutionAuthor, Project, Venue


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors', 'paper_access', 'data_access', 'code_access')
    exclude = ('slug',)


# Register your models here.
admin.site.register(Author)
admin.site.register(Institution)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Venue)
admin.site.register(InstitutionAuthor)
