from django.contrib.auth import get_user_model
from django.db import models

from ..base.models import TimeStampedModel
from ..admin_settings.models import State, City, Employee, Court


class Customer(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="customer_user")
    name = models.CharField(max_length=1024, blank=True, null=True, default='')
    mobile = models.CharField(max_length=1024, blank=True, null=True, default='')
    email = models.CharField(max_length=1024, blank=True, null=True)
    father_name = models.CharField(max_length=1024, blank=True, null=True)
    aadhar_no = models.CharField(max_length=1024, blank=True, null=True)
    pan_no = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    pincode = models.CharField(max_length=254, blank=True, null=True)
    is_aadhar_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Case(TimeStampedModel):
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.PROTECT,
                                 related_name="case_employee")
    accused = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT,
                                related_name="case_accused")
    victim = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT,
                               related_name="case_victim")
    court = models.ForeignKey(Court, blank=True, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="case_user")
    title = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    previous_hearing_date = models.DateField(blank=True, null=True)
    next_hearing_date = models.DateField(blank=True, null=True)
    next_hearing_time = models.TimeField(blank=True, null=True)
    prosecutor_lawyer = models.CharField(max_length=1024, blank=True, null=True)
    defender_lawyer = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)
