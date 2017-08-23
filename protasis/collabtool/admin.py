from django.contrib import admin
from .models import Author, Institution, InstitutionAuthor, Paper, Venue


class PaperAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors', 'paper_access', 'data_access', 'code_access')
    exclude = ('slug',)


# Register your models here.
admin.site.register(Author)
admin.site.register(Institution)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Venue)
admin.site.register(InstitutionAuthor)
