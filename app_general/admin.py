from django.contrib import admin

from . models import *

from import_export.admin import ExportActionMixin

from .resources import *

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','code','name']

admin.site.register(CourseModel, CourseAdmin)

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['product_id','course','generation','date_start','class_type']
    list_filter = ['product_id','course','class_type','generation',]

admin.site.register(ClassroomModel, ClassroomAdmin)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ['id','classroom','voucher_code','margin']
    list_filter = ['classroom',]

admin.site.register(VoucherModel, VoucherAdmin)

class RegisterAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['invoice_number','classroom','email','name','lastname','timestamp']
    list_filter = ['classroom','channel','receipt','paymenttype','paywithvoucher','timestamp',]
    search_fields = ['invoice_number',]
    resource_class = ClassroomResource

admin.site.register(RegisterModel, RegisterAdmin)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channel',]

admin.site.register(ChannelModel, ChannelAdmin)