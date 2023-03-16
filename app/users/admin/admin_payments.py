from django.contrib import admin
from ..models.models_payments import PaymentMethod, PaymentType

admin.site.register(PaymentMethod)
admin.site.register(PaymentType)
