from django.contrib import admin
from .models import (
    Author, Institution, InstitutionAuthor,
    Venue, Project, Publication,
    GroupAccess, Code, Data, PublicationBase)
from django.contrib.contenttypes.admin import GenericStackedInline
from genericadmin.admin import GenericAdminModelAdmin


class PublicationInline(GenericStackedInline):
    model = Publication


class PublicationAdmin(GenericAdminModelAdmin):
    # filter_horizontal = ('authors',)  # 'pa_paper_access', 'pa_data_access', 'pa_code_access')
    content_type_whitelist = ['collabtool/' + m.__name__.lower() for m in PublicationBase.iter_subclasses()]


class ProjectAdmin(admin.ModelAdmin):
    # inlines = [PublicationInline, ]
    filter_horizontal = ('institutions', 'publication', 'code', 'data')  # 'wp_paper_access', 'wp_data_access', 'wp_code_access')
    prepopulated_fields = {"slug": ("title",)}


class GroupAccessAdmin(admin.ModelAdmin):
    exclude = ('write',)


class FileAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    exclude = ('sha512', )

    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = False
        return perms


admin.site.register(Author)
admin.site.register(Institution)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Venue)
admin.site.register(InstitutionAuthor)
admin.site.register(GroupAccess)
admin.site.register(Code, FileAdmin)
admin.site.register(Data, FileAdmin)
admin.site.register(Publication, PublicationAdmin)


class PubItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors',)  # 'pa_paper_access', 'pa_data_access', 'pa_code_access')
    exclude = ('slug', 'sha512')

for m in PublicationBase.iter_subclasses():
    admin.site.register(m, PubItemAdmin)
