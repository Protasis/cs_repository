from django.contrib import admin
from .models import (
    Author, Institution, InstitutionAuthor,
    Paper, Venue, Project, WhitePaper,
    GroupAccess, Code, Data)


class PaperAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors',)  # 'pa_paper_access', 'pa_data_access', 'pa_code_access')
    exclude = ('slug',)


class WhitePaperAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors',)  # 'wp_paper_access', 'wp_data_access', 'wp_code_access')
    exclude = ('slug',)


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('institutions',)  # 'wp_paper_access', 'wp_data_access', 'wp_code_access')
    exclude = ('slug',)


class GroupAccessAdmin(admin.ModelAdmin):
    exclude = ('write',)


class CodeDataAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}

    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = False
        return perms


# TODO: fix view to only show Data/Code added for a given project
# Register your models here.
admin.site.register(Author)
admin.site.register(Institution)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(WhitePaper, WhitePaperAdmin)
admin.site.register(Venue)
admin.site.register(InstitutionAuthor)
admin.site.register(GroupAccess)
admin.site.register(Code, CodeDataAdmin)
admin.site.register(Data, CodeDataAdmin)
