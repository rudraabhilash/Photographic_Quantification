from django.db import models

class payments(models.Model):
  Name = models.CharField(max_length=255)
  Remarks = models.CharField(max_length=255)
  contact = models.IntegerField(null=True)
  emailID  = models.CharField(max_length=255)
  consulatationFee = models.IntegerField(null=True)

