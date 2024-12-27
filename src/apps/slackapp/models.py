from django.db import models

# Create your models here.
class SlackWorkspace(models.Model):
    team_id = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    bot_user_id = models.CharField(max_length=255, null=True, blank=True)
    installed_at = models.DateTimeField(auto_now_add=True)

