from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
# Create your models here.
import time
from django.utils import timezone


class Blog(models.Model):
    # user = models.ForeignKey('auth.User', related_name='blog', on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    modified_at = models.DateTimeField(auto_now=True)
    createdAt = UnixTimeStampField(auto_now_add=True)
    class Meta:
        ordering = ['createdAt']

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)