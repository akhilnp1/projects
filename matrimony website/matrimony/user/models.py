from django.db import models
from account.models import User
# Create your models here.

class PersonalDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='personaldetails')
    fathers_name = models.CharField(max_length=255, blank=False,default='Unknown')
    fathers_job = models.CharField(max_length=255, blank=False,default='sales')
    mothers_name = models.CharField(max_length=255, blank=False,default='Unknown')
    mothers_job = models.CharField(max_length=255, blank=False,default='sales')
    siblings = models.PositiveIntegerField(default=0)
    income = models.PositiveIntegerField( blank=False,default=0)
    height = models.PositiveIntegerField( blank=False,default=0)
    weight = models.PositiveIntegerField(blank=False,default=0)
    caste = models.CharField(max_length=255, blank=False)
    religion = models.CharField(max_length=255, blank=False)
    horriscope = models.FileField(upload_to='horoscopes/')
    permanent_address=models.TextField(default='Unknown')
    present_address=models.TextField(default='Unknown')
    country=models.CharField(
        max_length=10,
        blank=False,
        verbose_name='country',
        default='NONE',
        choices=[('INDIA','India')]
    )
    state=models.CharField(
        max_length=100,
        blank=False,
        verbose_name='state',
        default='NONE',
        choices=[('KERALA','Kerala'),('TAMILNADU','Tamilnadu')]
    )
    district=models.CharField(
        max_length=100,
        blank=False,
        verbose_name='district',
        default='NONE',
        choices=[('WAYANAD','Wayanad'),('THRISSUR','Thrissur'),('THIRUVANANTHAPURAM','Thiruvananthapuram'),('PATHANAMTHITTA','Pathanamthitta')
                 ,('PALAKKAD','Palakkad'),('MALAPPURAM','Malappuram'),('KOTTAYAM','Kottayam'),('KOLLAM','Kollam')
                 ,('KOZHIKODE','Kozhikode'),('KASARKODE','Kasarkode'),('IDUKKI','Idukki'),('ERNAKULAM','Ernakulam'),('ALAPPUZHA','Alappuzha')]
    )
    caste = models.CharField( max_length=100,choices=[ ('Brahmin', 'Brahmin'), ('Kshatriya', 'Kshatriya'), ('Vaishya', 'Vaishya'),
    ('Shudra', 'Shudra'), ('Dalit', 'Dalit'), ('Koli', 'Koli'), ('Gujar', 'Gujar'),
    ('Lodhi', 'Lodhi'), (' Yadav', 'Yadav'), ('Jat', 'Jat') ,('Others','Others')]
    )

    religion = models.CharField(max_length=100,choices=[ ('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Hinduism', 'Hinduism'),
    ('Buddhism', 'Buddhism'), ('Sikhism', 'Sikhism'), ('Judaism', 'Judaism'), ('Baha’i', 'Baha’i'), ('Jainism', 'Jainism'),
    ('Shintoism', 'Shintoism'), ('Cao Dai', 'Cao Dai'),('Others','Others')])

    def is_filled(self):
        print("Checking if all fields are filled:")
        
        # Check if all required fields are properly filled
        all_filled = True

        fields_to_check = {
            "Fathers Name": self.fathers_name,
            "Fathers Job": self.fathers_job,
            "Mothers Name": self.mothers_name,
            "Mothers Job": self.mothers_job,
            "Siblings": self.siblings,
            "Income": self.income,
            "Height": self.height,
            "Weight": self.weight,
            "Caste": self.caste,
            "Religion": self.religion,
            "Permanent Address": self.permanent_address,
            "Present Address": self.present_address,
            "Country": self.country,
            "State": self.state,
            "District": self.district
        }

        for field_name, value in fields_to_check.items():
            if value is None or (isinstance(value, str) and value.strip() == '') or (isinstance(value, int) and value <= 0):
                print(f"{field_name} is not filled or has invalid value: {value}")
                all_filled = False

        # Ensure file field is provided
        file_filled = self.horriscope and self.horriscope.name != 'unknown'
        if not file_filled:
            print("Horoscope file is not provided or has invalid value.")

        print(f"Is filled: {all_filled and file_filled}")
        
        return all_filled and file_filled

    
   

class PartnerPreferance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_preference')
    age_min = models.PositiveIntegerField(default=18)
    age_max = models.PositiveIntegerField(default=40)
    caste = models.CharField(max_length=100,choices=[ ('Brahmin', 'Brahmin'), ('Kshatriya', 'Kshatriya'), ('Vaishya', 'Vaishya'),
    ('Shudra', 'Shudra'), ('Dalit', 'Dalit'), ('Koli', 'Koli'), ('Gujar', 'Gujar'),
    ('Lodhi', 'Lodhi'), (' Yadav', 'Yadav'), ('Jat', 'Jat') ,('Others','Others')]
)
    religion = models.CharField(max_length=100,choices=[ ('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Hinduism', 'Hinduism'),
    ('Buddhism', 'Buddhism'), ('Sikhism', 'Sikhism'), ('Judaism', 'Judaism'), ('Baha’i', 'Baha’i'), ('Jainism', 'Jainism'),
    ('Shintoism', 'Shintoism'), ('Cao Dai', 'Cao Dai'),('Others','Others')])
    height_min = models.PositiveIntegerField(default=120)
    height_max = models.PositiveIntegerField(default=180)
    weight_min = models.PositiveIntegerField(default=50)
    weight_max = models.PositiveIntegerField(default=100)
    income_min = models.PositiveIntegerField(default=10000)
    income_max = models.PositiveIntegerField(default=200000)
    gender = models.CharField(default='Male',max_length=20,choices=[ ('MALE', 'Male'),('FEMALE', 'Female')])
    qualification = models.CharField(
        default='PLUSTWO',
        max_length=50,
        choices=[
            ('SSLC', 'SSLC'),
            ('PLUSTWO', 'Plus Two'),
            ('BACHELOR', 'Bachelors'),
            ('MASTERS', 'Masters'),
            ('PHD', 'PhD'),
            ('BCOM', 'bcom'),
        ]
    )

    def __str__(self):
        return self.user.username
    
    def is_filled(self):
        required_fields = [
            self.age_min, self.age_max, self.caste, self.religion,
            self.height_min, self.height_max, self.weight_min,
            self.weight_max, self.income_min, self.income_max,
            self.gender, self.qualification
        ]
        return all(bool(field) for field in required_fields)
    

    


class FriendRequest(models.Model):
    id = models.BigAutoField(primary_key=True)  # Using BigAutoField for the primary key
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # Sets the timestamp when the request is created
    updated_at = models.DateTimeField(auto_now=True)  # Updates the timestamp every time the object is saved
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.sender} to {self.recipient}'

# Optionally, create a Conversation model
class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return f'Conversation between {", ".join([user.username for user in self.participants.all()])}'
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.username} -> {self.favorite.username}"
    


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255,default="")  # Store the product name
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=10)  # Store the amount
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.stripe_subscription_id} - {self.product_name}"