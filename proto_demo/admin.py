from django.contrib import admin

from models import Maker, Project, Category, Major
# Register your models here.

class MakerAdmin(admin.ModelAdmin):
    list_display = ['pk','user','profile_pic',]
    list_filter = ['maker_major','maker_related_category']

class MakerInline(admin.TabularInline):
    model = Project.project_starter.through

class ProjectlAdmin(admin.ModelAdmin):
    fields = ('project_name','project_category','project_starter','project_request_major','project_detail','project_file')
    list_display = ('pk','project_name','project_category','pub_date')
    list_filter = ('project_starter','project_category','project_request_major')
    inlines = [MakerInline]
#class CategoryInline(admin.TabularInline):
#    model = Major.major_relate_category.through
#    extra = 1
class MajorAdmin(admin.ModelAdmin):
    fields = (
        'major_name',
    )






admin.site.register(Maker,MakerAdmin)
admin.site.register(Project,ProjectlAdmin)
admin.site.register(Category,)
admin.site.register(Major,MajorAdmin)