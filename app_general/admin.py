from django.contrib import admin

from . models import *

from import_export.admin import ExportActionMixin

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['code','name']

admin.site.register(CourseModel, CourseAdmin)

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['id','course','generation','date_start','class_type']

admin.site.register(ClassroomModel, ClassroomAdmin)

class RegisterAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['classroom','email','name','lastname','timestamp']
    list_filter = ['channel','receipt','paymenttype','paywithvoucher','timestamp',]
    search_fields = ['classroom',]

admin.site.register(RegisterModel, RegisterAdmin)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channel',]

admin.site.register(ChannelModel, ChannelAdmin)