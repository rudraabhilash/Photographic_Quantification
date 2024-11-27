from django.db import models

class doctorinfo(models.Model):
  docName = models.CharField(max_length=255)
  expertise = models.CharField(max_length=255)
  contact = models.IntegerField(null=True)
  emailID  = models.CharField(max_length=255)
  description = models.CharField(max_length=500)
  department = models.CharField(max_length=500)
  consulatationFee = models.IntegerField(null=True)

