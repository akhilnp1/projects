# Generated by Django 5.0.6 on 2024-07-04 20:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.CharField(blank=True, max_length=255)),
                ('height', models.CharField(blank=True, max_length=255)),
                ('weight', models.CharField(blank=True, max_length=255)),
                ('caste', models.CharField(blank=True, max_length=255)),
                ('religion', models.CharField(blank=True, max_length=255)),
                ('horriscope', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personaldet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
