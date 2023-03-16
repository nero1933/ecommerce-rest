from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PaymentMethod(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    payment_type = models.ForeignKey('PaymentType', on_delete=models.CASCADE)
    account_number = models.PositiveIntegerField()
    expiry_date = models.DateField()
    security_code = models.PositiveIntegerField() # Add validator to check for 001 - 999 range
    is_default = models.BooleanField(default=False)


class PaymentType(models.Model):
    payment_type = models.CharField(max_length=50)
