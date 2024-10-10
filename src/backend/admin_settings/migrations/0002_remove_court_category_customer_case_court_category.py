# Generated by Django 4.2.7 on 2023-11-30 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='court',
            name='category',
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('mobile', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('emails', models.CharField(blank=True, max_length=1024, null=True)),
                ('phone_numbers', models.CharField(blank=True, max_length=1024, null=True)),
                ('fathers_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('pan_number', models.CharField(blank=True, max_length=1024, null=True)),
                ('image', models.CharField(blank=True, max_length=1024, null=True)),
                ('address', models.CharField(blank=True, max_length=1024, null=True)),
                ('pincode', models.CharField(blank=True, max_length=254, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.city')),
                ('court', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.court')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer_partner', to='admin_settings.employee')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='court',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admin_settings.dynamicsettings'),
        ),
    ]
