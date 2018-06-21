from django.contrib import admin
from .models import TargetUsers, Followers, LoginData, TargetHashTags, TargetedHashTagUsers

# Register your models here.
admin.site.register(LoginData)

admin.site.register(TargetUsers)

admin.site.register(Followers)

admin.site.register(TargetHashTags)

admin.site.register(TargetedHashTagUsers)