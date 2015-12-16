from django.contrib import admin
from models import*
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profilsdfae'

class LocalUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class VrstvaAdmin(admin.ModelAdmin):
    list_display = ["nazov","nahodnaFarba"]

# Register your models here.
admin.site.register(Zapis);
admin.site.register(Vrstva,VrstvaAdmin)
admin.site.register(DiskusnyPrispevok)
admin.site.unregister(User)
admin.site.register(User,LocalUserAdmin)
admin.site.register(Napad)
admin.site.register(Team)