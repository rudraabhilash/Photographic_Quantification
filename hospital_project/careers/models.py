from django.db import models

class positions(models.Model):
  positionName = models.CharField(max_length=255)
  hrName = models.CharField(max_length=255)
  openingDate = models.DateField(null=True)
  closedDate  = models.DateField(null=True)
  notes = models.CharField(max_length=500)
  status = models.IntegerField(null=True)
  department = models.CharField(max_length=500)
  baseSalary = models.IntegerField(null=True)
  HiringManager = models.CharField(max_length=255)

