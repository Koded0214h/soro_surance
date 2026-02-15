from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with additional fields for insurance platform"""
    
    class UserType(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        AGENT = 'agent', _('Agent')
        ADMIN = 'admin', _('Admin')
        REVIEWER = 'reviewer', _('Reviewer')
    
    phone_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(
        max_length=20, 
        choices=UserType.choices, 
        default=UserType.CUSTOMER
    )
    date_of_birth = models.DateField(null=True, blank=True)
    bvn = models.CharField(max_length=11, blank=True, null=True)  # Bank Verification Number
    nin = models.CharField(max_length=11, blank=True, null=True)  # National Identity Number
    
    # Contact Information
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lga = models.CharField(max_length=100, blank=True, null=True)  # Local Government Area
    
    # Insurance specific
    soro_score = models.FloatField(default=50.0)  # Initial risk score
    total_claims = models.IntegerField(default=0)
    approved_claims = models.IntegerField(default=0)
    rejected_claims = models.IntegerField(default=0)
    
    # Payment Information
    bank_account_number = models.CharField(max_length=10, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Communication preferences
    prefers_voice = models.BooleanField(default=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Groups And Permissions
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
    
    username = None  # Remove username field
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager() # Custom Manager
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.phone_number})"
    
    @property
    def full_name(self):
        return self.get_full_name()
    
    @property
    def risk_level(self):
        if self.soro_score <= 30:
            return 'low'
        elif self.soro_score <= 70:
            return 'medium'
        else:
            return 'high'


class UserProfile(models.Model):
    """Extended profile information for customers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Demographic Information
    occupation = models.CharField(max_length=200, blank=True, null=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    
    # Insurance History
    has_previous_insurance = models.BooleanField(default=False)
    previous_insurer = models.CharField(max_length=200, blank=True, null=True)
    years_with_previous_insurer = models.IntegerField(default=0)
    
    # Vehicle Information (for motor insurance)
    vehicle_make = models.CharField(max_length=100, blank=True, null=True)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    vehicle_year = models.IntegerField(null=True, blank=True)
    vehicle_registration = models.CharField(max_length=50, blank=True, null=True)
    
    # Property Information (for property insurance)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    property_address = models.TextField(blank=True, null=True)
    property_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Health Information (for health insurance)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.get_full_name()}"


class UserActivity(models.Model):
    """Track user activities and interactions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.activity_type}"