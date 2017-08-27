from django.contrib import admin
from .models import Author, Institution, InstitutionAuthor, Paper, Venue, Project, WhitePaper


class PaperAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors', 'pa_paper_access', 'pa_data_access', 'pa_code_access')
    exclude = ('slug',)


class WhitePaperAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors', 'wp_paper_access', 'wp_data_access', 'wp_code_access')
    exclude = ('slug',)


# TODO: fix view to only show Data/Code added for a given project
# Register your models here.
admin.site.register(Author)
admin.site.register(Institution)
admin.site.register(Project)
admin.site.register(Paper, PaperAdmin)
admin.site.register(WhitePaper, WhitePaperAdmin)
admin.site.register(Venue)
admin.site.register(InstitutionAuthor)
