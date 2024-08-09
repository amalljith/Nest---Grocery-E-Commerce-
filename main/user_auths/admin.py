from django.contrib import admin
from .models import Users, ContactUs, Profile

class UserAdmin(admin.ModelAdmin):
    list_display =['username','email','bio']


class ContactUsAdmin(admin.ModelAdmin):
    list_display =['full_name','email','subject']


# class ProfileUsAdmin(admin.ModelAdmin):
#     list_display =['user','full_name','bio','phone']

admin.site.register(Users,UserAdmin)
admin.site.register(ContactUs,ContactUsAdmin)
admin.site.register(Profile)