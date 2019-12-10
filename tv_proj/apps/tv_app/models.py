from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime

class TvManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 2:
            errors["title"] = "Title must be at least 1 characters."
        if len(postData["network"]) < 3:
            errors["network"] = "Network must be at least 5 characters."
        if postData["desc"]:
            if len(postData["desc"]) < 10:
                errors["desc"] = "Description must be at least 10 characters."
        if len(postData["release_date"]) > 0 and datetime.strptime(postData["release_date"], '%Y-%m-%d') > datetime.today() :
            errors["release_date"] = "Invalid release date."
        return errors

class TV(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    desc = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TvManager()
# Create your models here.

