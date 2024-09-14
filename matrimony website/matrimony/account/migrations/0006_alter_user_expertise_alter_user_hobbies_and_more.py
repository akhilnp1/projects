# Generated by Django 5.0.6 on 2024-07-07 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_expertise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=models.CharField(blank=True, choices=[('B', 'Beginner'), ('I', 'Intermediate'), ('E', 'Expert')], default='I', max_length=1, verbose_name='Expertise'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hobbies',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='interests',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='qualification',
            field=models.CharField(max_length=255),
        ),
    ]
