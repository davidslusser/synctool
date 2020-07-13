from django.db import models

# Create your models here.


class PersonOne(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32, blank=True, null=True)


class PersonTwo(models.Model):
    fname = models.CharField(max_length=32)
    lname = models.CharField(max_length=32)
    phone = models.CharField(max_length=32, blank=True, null=True)


class CabinetOne(models.Model):
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32, blank=True, null=True)


class CabinetTwo(models.Model):
    cab_name = models.CharField(max_length=32)
    room = models.CharField(max_length=32, blank=True, null=True)
