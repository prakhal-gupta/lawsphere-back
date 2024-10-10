from django.contrib.auth import get_user_model
from django.db import models

from .constants import TRANSACTION_TYPES, CREDIT, DEBIT, PROFESSIONS, employee_STATUS, BLOOD_GROUPS, ACTIVE
from ..base.models import TimeStampedModel, upload_file
from ..base.validators.form_validations import file_extension_validator


class DynamicSettings(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    icon = models.CharField(max_length=1024, blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_editable = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    is_deletable = models.BooleanField(default=True)

    class Meta:
        ordering = ['value']


class UploadedDocument(TimeStampedModel):
    name = models.CharField(max_length=1000, blank=True, null=True)
    image = models.FileField(upload_to=upload_file, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def image_path(self):
        return self.image.name


class Country(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    country_code = models.CharField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class State(TimeStampedModel):
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=1024, blank=True, null=True)
    state_code = models.CharField(max_length=255, blank=True, null=True)
    is_territorial = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']


class City(TimeStampedModel):
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']


class Documents(TimeStampedModel):
    document_type = models.CharField(max_length=1024, blank=True, null=True)
    document_format = models.CharField(max_length=1024, blank=True, null=True)
    file = models.CharField(max_length=1024, blank=True, null=True)
    file_label = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_return = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class Court(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(DynamicSettings, blank=True, null=True, on_delete=models.PROTECT)
    manager = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                                related_name="court_manager")
    documents = models.ManyToManyField(Documents, blank=True)
    is_active = models.BooleanField(default=True)


class EmployeePermissions(TimeStampedModel):
    key = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)


# designation wise permission/permission sets
class PermissionSets(TimeStampedModel):
    court = models.ForeignKey(Court, blank=True, null=True, on_delete=models.PROTECT)
    employee = models.ForeignKey('admin_settings.Employee', blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(EmployeePermissions, blank=True)
    is_disabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class Employee(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="employee_user")
    court = models.ForeignKey(Court, blank=True, null=True, on_delete=models.PROTECT)
    permissions = models.ManyToManyField(EmployeePermissions, blank=True)
    first_name = models.CharField(max_length=128, blank=True, null=True, default='')
    last_name = models.CharField(max_length=128, blank=True, null=True, default='')
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=128, blank=True, null=True, default='')
    mobile2 = models.CharField(max_length=128, blank=True, null=True, default='')
    permission_set = models.ForeignKey(PermissionSets, blank=True, null=True, on_delete=models.PROTECT,
                                       related_name="employee_permission_set")
    designation = models.ForeignKey(DynamicSettings, blank=True, null=True, on_delete=models.PROTECT, related_name="employee_designation")
    department = models.ForeignKey(DynamicSettings, blank=True, null=True, on_delete=models.PROTECT, related_name="employee_department")
    photo = models.CharField(max_length=1024, blank=True, null=True)
    emp_code = models.CharField(max_length=124, blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=employee_STATUS, default=ACTIVE, max_length=124, null=True)
    """documents"""
    aadhaar_no = models.CharField(max_length=1024, blank=True, null=True)
    pan_no = models.CharField(max_length=1024, blank=True, null=True)
    dl_no = models.CharField(max_length=1024, blank=True, null=True)
    passport = models.CharField(max_length=1024, blank=True, null=True)
    blood_group = models.CharField(choices=BLOOD_GROUPS, max_length=24, blank=True, null=True)
    documents = models.ManyToManyField(Documents, blank=True)
    is_primary = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class CsvPdfReports(TimeStampedModel):
    rep_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    report_upload = models.FileField(upload_to="law-reports/%Y/%m/%d", max_length=80, blank=True, null=True,
                                     validators=[file_extension_validator])


class DescriptionTemplate(TimeStampedModel):
    service = models.ForeignKey(DynamicSettings, blank=True, null=True, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Customer(TimeStampedModel):
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.PROTECT,
                                related_name="customer_partner")
    court = models.ForeignKey(Court, blank=True, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="customer_user")
    first_name = models.CharField(max_length=128, blank=True, null=True, default='')
    mobile = models.CharField(max_length=128, blank=True, null=True, default='')
    emails = models.CharField(max_length=1024, blank=True, null=True)
    phone_numbers = models.CharField(max_length=1024, blank=True, null=True)
    fathers_name = models.CharField(max_length=1024, blank=True, null=True)
    pan_number = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    pincode = models.CharField(max_length=254, blank=True, null=True)
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
    is_active = models.BooleanField(default=True)