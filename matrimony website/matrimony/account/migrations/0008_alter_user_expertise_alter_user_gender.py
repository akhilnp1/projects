# Generated by Django 5.0.6 on 2024-07-09 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_date_of_birth_alter_user_hobbies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=models.CharField(blank=True, choices=[('BEGINNER', 'Beginner'), ('IINTERMEDIATE', 'Intermediate'), ('EXPERT', 'Expert')], default='I', max_length=100, verbose_name='Expertise'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHERS', 'Other')], default='MALE', max_length=10, verbose_name='Gender'),
        ),
    ]