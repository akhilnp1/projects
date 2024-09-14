# Generated by Django 5.0.6 on 2024-07-04 21:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_parentsdetails'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerPreferance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(blank=True, max_length=255)),
                ('caste', models.CharField(blank=True, max_length=255)),
                ('religion', models.CharField(blank=True, max_length=255)),
                ('height', models.CharField(blank=True, max_length=255)),
                ('weight', models.CharField(blank=True, max_length=255)),
                ('income', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='partnerpre', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
