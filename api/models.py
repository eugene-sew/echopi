from django.db import models

# Create your models here.

class Device(models.Model):
    mac_address = models.CharField(max_length=17, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=50)
    power_level = models.FloatField()
    temperature = models.FloatField()
    uptime = models.DurationField()
    ip_address = models.GenericIPAddressField()

class Deployment(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_number = models.CharField(max_length=20)
    forest_name = models.CharField(max_length=100)

class Alert(models.Model):
    ALERT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RESOLVED', 'Resolved'),
        ('FALSE_ALARM', 'False Alarm'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    report_details = models.TextField()
    status = models.CharField(max_length=20, choices=ALERT_STATUS_CHOICES, default='PENDING')
