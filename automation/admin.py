from django.contrib import admin
from .models import TargetUsers, Followers, LoginData, TargetHashTags, TargetedHashTagUsers, UserConfigurationsState

class FollowersAdmin(admin.ModelAdmin):
    list_display = ('uname_id', 'is_processed')
# Register your models here.


admin.site.register(LoginData)

admin.site.register(TargetUsers)

admin.site.register(Followers, FollowersAdmin)

admin.site.register(TargetHashTags)

admin.site.register(TargetedHashTagUsers)

admin.site.register(UserConfigurationsState)
