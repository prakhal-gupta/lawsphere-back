# Generated by Django 4.2.7 on 2023-11-28 06:14

import backend.base.models
import backend.base.validators.form_validations
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('country_code', models.CharField(blank=True, max_length=256, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('document_type', models.CharField(blank=True, max_length=1024, null=True)),
                ('document_format', models.CharField(blank=True, max_length=1024, null=True)),
                ('file', models.CharField(blank=True, max_length=1024, null=True)),
                ('file_label', models.CharField(blank=True, max_length=1024, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_return', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('mobile2', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('designation', models.CharField(blank=True, max_length=1024, null=True)),
                ('department', models.CharField(blank=True, max_length=1024, null=True)),
                ('photo', models.CharField(blank=True, max_length=1024, null=True)),
                ('emp_code', models.CharField(blank=True, max_length=124, null=True)),
                ('current_address', models.TextField(blank=True, null=True)),
                ('permanent_address', models.TextField(blank=True, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Deactive', 'Deactive'), ('Abscond', 'Abscond'), ('Retired', 'Retired'), ('Leaved', 'Active')], default='Active', max_length=124, null=True)),
                ('aadhaar_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('pan_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('dl_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('passport', models.CharField(blank=True, max_length=1024, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=24, null=True)),
                ('emergency_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('emergency_mobile1', models.CharField(blank=True, max_length=1024, null=True)),
                ('emergency_mobile2', models.CharField(blank=True, max_length=1024, null=True)),
                ('relationship', models.CharField(blank=True, max_length=1024, null=True)),
                ('emergency_address', models.TextField(blank=True, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_disabled', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('court', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.court')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('documents', models.ManyToManyField(blank=True, to='admin_settings.documents')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeePermissions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('key', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UploadedDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to=backend.base.models.upload_file)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('state_code', models.CharField(blank=True, max_length=255, null=True)),
                ('is_territorial', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.country')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PermissionSets',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_disabled', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('court', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.court')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.employee')),
                ('permissions', models.ManyToManyField(blank=True, to='admin_settings.employeepermissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='permission_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee_permission_set', to='admin_settings.permissionsets'),
        ),
        migrations.AddField(
            model_name='employee',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='admin_settings.employeepermissions'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DynamicSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=1024, null=True)),
                ('icon', models.CharField(blank=True, max_length=1024, null=True)),
                ('value', models.CharField(blank=True, max_length=1024, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_editable', models.BooleanField(default=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('is_deletable', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_settings.dynamicsettings')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='DescriptionTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.dynamicsettings')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CsvPdfReports',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('rep_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('report_upload', models.FileField(blank=True, max_length=80, null=True, upload_to='law-reports/%Y/%m/%d', validators=[backend.base.validators.form_validations.file_extension_validator])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='court',
            name='category',
            field=models.ManyToManyField(blank=True, to='admin_settings.dynamicsettings'),
        ),
        migrations.AddField(
            model_name='court',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.city'),
        ),
        migrations.AddField(
            model_name='court',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.country'),
        ),
        migrations.AddField(
            model_name='court',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='court',
            name='documents',
            field=models.ManyToManyField(blank=True, to='admin_settings.documents'),
        ),
        migrations.AddField(
            model_name='court',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='court_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='court',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.state'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.state'),
        ),
    ]
