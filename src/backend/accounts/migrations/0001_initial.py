# Generated by Django 5.1.3 on 2024-11-22 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('middle_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('mobile', models.CharField(blank=True, max_length=128, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('pan_no', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('username', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('date_joined', models.DateField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('personal_storage', models.FloatField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_separated', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='OTPLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('otp', models.CharField(blank=True, max_length=15, null=True)),
                ('counter', models.IntegerField(blank=True, default=25)),
                ('is_active', models.BooleanField(default=True)),
                ('resend_counter', models.IntegerField(blank=True, default=25)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('uid', models.CharField(default='uidrequired', max_length=1024)),
                ('timestamp', models.CharField(default='timestamprequired', max_length=1024)),
                ('signature', models.CharField(default='signaturerequired', max_length=1024)),
                ('code', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='User_Abstract', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
