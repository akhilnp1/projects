# Generated by Django 5.0.6 on 2024-07-04 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_expertise_user_job_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=models.CharField(choices=[('B', 'Beginner'), ('I', 'Intermediate'), ('E', 'Expert')], default='', max_length=1, verbose_name='Expertise'),
        ),
    ]
