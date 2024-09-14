from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from datetime import date


class User(AbstractUser):

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHERS', 'Other'),
    )
    EXPERTISE_CHOICES = (
        ('BEGINNER', 'Beginner'),
        ('IINTERMEDIATE', 'Intermediate'),
        ('EXPERT', 'Expert'),
    )
    INTERESTS_CHOICES = (
        ('READING', 'Reading'),
        ('WRITING', 'Writing'),
        ('MUSIC', 'Music'),
        ('OTHERS', 'Others'),
    )

    HOBBIES_CHOICES = (
        ('DANCE', 'Dance'),
        ('TRAVEL', 'Travel'),
        ('FOOTBALL', 'Football'),
        ('CRICKET', 'Cricket'),
        ('OTHER', 'Other_activities'),
    )

    
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        blank=True, 
        verbose_name='Profile photo'
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=False, 
        verbose_name='Date of birth'
    )
    gender = models.CharField(
        max_length=10, 
        choices=GENDER_CHOICES, 
        blank=False, 
        verbose_name='Gender',
        default='MALE'
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True, 
        blank=True,
        null=True,
        verbose_name='Phone number'
    )
    age = models.PositiveIntegerField(null=True, blank=True)

    hobbies = models.TextField(max_length=255, blank=False)
    interests = models.TextField(max_length=255, blank=False)
    smoking_status = models.CharField(max_length=20,default='Non-smoker', choices=[('Non-smoker', 'Non-smoker'),('Smoker', 'Smoker'),('Occasional', 'Occasional'),])
    drinking_status = models.CharField(max_length=20,default='Non-drinker', choices=[('Non-drinker', 'Non-drinker'),('Drinker', 'Drinker'),('Occasional', 'Occasional'),])

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        super(User, self).save(*args, **kwargs)

    qualification = models.CharField(max_length=255, blank=False
                                     ,choices=[('SSLC', 'SSLC'), ('PLUSTWO', 'PLUSTWO'), ('BACHELOR', 'BACHELOR'), ('MASTERS', 'MASTERS'), ('PHD', 'PHD')]
)

    company_name = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    job_title = models.CharField(max_length=255, blank=True)
    expertise = models.CharField(
        max_length=100, 
        choices=EXPERTISE_CHOICES, 
        blank=True, 
        verbose_name='Expertise',
        default=''
    )

    
    @property
    def is_basic_profile_complete(self):
        """
        Determines if the basic profile is complete by checking all the fields.

        Returns:
            bool: True if the user has filled all the required fields, False otherwise.
        """
        return all([
            self.first_name,
            self.last_name,
            self.email,
            self.password,
            self.username,
            self.phone_number,
            self.profile_photo,
            self.date_of_birth,
            self.age,
            self.gender,
            self.hobbies,
            self.interests,
            self.qualification,
            self.company_name,
            self.designation,
            self.location,
            self.job_title,
            self.expertise,
        ])
