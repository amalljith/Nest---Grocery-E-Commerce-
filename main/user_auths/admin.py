from django.contrib import admin
from .models import Users, ContactUs

class UserAdmin(admin.ModelAdmin):
    list_display =['username','email','bio']


class ContactUsAdmin(admin.ModelAdmin):
    list_display =['full_name','email','subject']

admin.site.register(Users,UserAdmin)
admin.site.register(ContactUs,ContactUsAdmin)