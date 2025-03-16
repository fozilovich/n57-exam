from django.contrib import admin
from app_payment.models import *

admin.site.register([Month,PaymentType,Payment])