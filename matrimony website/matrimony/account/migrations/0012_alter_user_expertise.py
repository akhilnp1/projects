# Generated by Django 5.0 on 2024-07-29 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_user_qualification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=models.CharField(blank=True, choices=[('BEGINNER', 'Beginner'), ('IINTERMEDIATE', 'Intermediate'), ('EXPERT', 'Expert')], default='', max_length=100, verbose_name='Expertise'),
        ),
    ]
