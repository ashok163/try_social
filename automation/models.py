from django.db import models
from datetime import datetime

class LoginData(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)


class TargetUsers(models.Model):
    users = models.CharField(max_length=120)
    login_user = models.ForeignKey(LoginData, on_delete=models.CASCADE)


class Followers(models.Model):
    targetusers = models.ForeignKey(TargetUsers, on_delete=models.CASCADE)
    uname_id = models.CharField(max_length=120)
    u_id = models.CharField(max_length=120, null=True)
    is_public = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)


class TargetHashTags(models.Model):
    htags = models.CharField(max_length=120)
    login_user = models.ForeignKey(LoginData, on_delete=models.CASCADE)


class TargetedHashTagUsers(models.Model):
    targethashtags = models.ForeignKey(TargetHashTags, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=120)


class UserConfigurationsState(models.Model):
    celeb_user_name = models.CharField(max_length=120)
    hash_tag = models.CharField(max_length=120)
    likes_per_hour = models.CharField(max_length=120)
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(auto_now_add=False, blank=True)


class UserFeedbackData(models.Model):
    liked_users = models.CharField(max_length=120)
    media_ids = models.CharField(max_length=120)


