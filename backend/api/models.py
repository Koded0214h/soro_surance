from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class InsuranceProduct(models.Model):
    """Insurance products offered by Sorosurance"""
    
    class ProductType(models.TextChoices):
        MOTOR = 'motor', _('Motor Insurance')
        HEALTH = 'health', _('Health Insurance')
        PROPERTY = 'property', _('Property Insurance')
        LIFE = 'life', _('Life Insurance')
        TRAVEL = 'travel', _('Travel Insurance')
    
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=50, choices=ProductType.choices)
    description = models.TextField()
    
    # Pricing
    base_premium = models.DecimalField(max_digits=10, decimal_places=2)
    min_premium = models.DecimalField(max_digits=10, decimal_places=2)
    max_premium = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Coverage
    coverage_details = models.JSONField(default=dict)
    exclusions = models.JSONField(default=list)
    
    # Requirements
    required_documents = models.JSONField(default=list)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()})"


class Policy(models.Model):
    """Insurance policy purchased by customer"""
    
    class PolicyStatus(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        ACTIVE = 'active', _('Active')
        EXPIRED = 'expired', _('Expired')
        CANCELLED = 'cancelled', _('Cancelled')
        PENDING = 'pending', _('Pending Payment')
    
    policy_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
    product = models.ForeignKey(InsuranceProduct, on_delete=models.PROTECT)
    
    # Policy Details
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=PolicyStatus.choices, default=PolicyStatus.DRAFT)
    
    # Risk Assessment
    initial_soro_score = models.FloatField()  # Score at policy creation
    current_soro_score = models.FloatField()  # Updated score
    
    # Premium Information
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium_frequency = models.CharField(max_length=20, default='monthly')  # monthly, quarterly, annually
    next_payment_date = models.DateField(null=True, blank=True)
    
    # Coverage
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    deductible_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_details = models.JSONField(default=dict)
    
    # Payment Information
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Policies'
    
    def __str__(self):
        return f"Policy {self.policy_number} - {self.user.get_full_name()}"
    
    @property
    def is_active(self):
        return self.status == self.PolicyStatus.ACTIVE
    
    @property
    def days_remaining(self):
        from django.utils import timezone
        if self.end_date:
            delta = self.end_date - timezone.now().date()
            return max(0, delta.days)
        return 0


class Claim(models.Model):
    """Insurance claim filed by customer"""
    
    class ClaimStatus(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        SUBMITTED = 'submitted', _('Submitted')
        UNDER_REVIEW = 'under_review', _('Under Review')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
        PAID = 'paid', _('Paid')
        CLOSED = 'closed', _('Closed')
    
    class ClaimType(models.TextChoices):
        ACCIDENT = 'accident', _('Accident')
        THEFT = 'theft', _('Theft')
        DAMAGE = 'damage', _('Damage')
        ILLNESS = 'illness', _('Illness')
        DEATH = 'death', _('Death')
        OTHER = 'other', _('Other')
    
    claim_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    
    # Claim Details
    claim_type = models.CharField(max_length=50, choices=ClaimType.choices)
    description = models.TextField()
    incident_date = models.DateField()
    incident_time = models.TimeField(null=True, blank=True)
    incident_location = models.CharField(max_length=500)
    
    # Claim Amount
    estimated_loss = models.DecimalField(max_digits=12, decimal_places=2)
    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deductible_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Voice Claim Data
    audio_file = models.FileField(upload_to='claim_audio/', null=True, blank=True)
    audio_duration = models.IntegerField(null=True, blank=True)  # in seconds
    transcript = models.TextField(null=True, blank=True)
    transcript_confidence = models.FloatField(null=True, blank=True)
    
    # AI Analysis
    soro_score = models.FloatField(null=True, blank=True)  # Claim-specific risk score
    risk_level = models.CharField(max_length=20, null=True, blank=True)  # low, medium, high
    sentiment_score = models.FloatField(null=True, blank=True)
    urgency_score = models.FloatField(null=True, blank=True)
    inconsistency_score = models.FloatField(null=True, blank=True)
    
    # Keywords extracted from voice
    keywords = models.JSONField(default=list, blank=True)
    
    # Media Evidence
    photos = models.JSONField(default=list, blank=True)  # List of photo URLs
    videos = models.JSONField(default=list, blank=True)  # List of video URLs
    documents = models.JSONField(default=list, blank=True)  # List of document URLs
    
    # Status and Processing
    status = models.CharField(max_length=20, choices=ClaimStatus.choices, default=ClaimStatus.DRAFT)
    auto_approval_recommended = models.BooleanField(default=False)
    review_notes = models.TextField(blank=True, null=True)
    
    # Reviewer Information
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='reviewed_claims')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Payment Information
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Claim {self.claim_number} - {self.get_claim_type_display()}"
    
    def save(self, *args, **kwargs):
        # Calculate risk level based on soro_score
        if self.soro_score is not None:
            if self.soro_score <= 30:
                self.risk_level = 'low'
            elif self.soro_score <= 70:
                self.risk_level = 'medium'
            else:
                self.risk_level = 'high'
        super().save(*args, **kwargs)


class VoiceAnalysis(models.Model):
    """Detailed analysis of voice claims"""
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE, related_name='voice_analysis')
    
    # Audio Features
    sample_rate = models.IntegerField(null=True, blank=True)
    channels = models.IntegerField(null=True, blank=True)
    bit_depth = models.IntegerField(null=True, blank=True)
    audio_format = models.CharField(max_length=20, null=True, blank=True)
    
    # Speech Analysis
    word_count = models.IntegerField(null=True, blank=True)
    speaking_rate = models.FloatField(null=True, blank=True)  # words per minute
    pause_frequency = models.FloatField(null=True, blank=True)
    filler_word_count = models.IntegerField(null=True, blank=True)
    
    # Sentiment Analysis
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)
    sentiment_scores = models.JSONField(default=dict, blank=True)
    
    # Emotion Detection
    emotion_scores = models.JSONField(default=dict, blank=True)
    
    # Voice Characteristics
    pitch_variance = models.FloatField(null=True, blank=True)
    volume_variance = models.FloatField(null=True, blank=True)
    speech_clarity = models.FloatField(null=True, blank=True)
    
    # Metadata Analysis
    recording_device = models.CharField(max_length=100, null=True, blank=True)
    background_noise_level = models.FloatField(null=True, blank=True)
    recording_quality = models.CharField(max_length=20, null=True, blank=True)
    
    # AI Flags
    flags = models.JSONField(default=list, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Voice Analysis for Claim {self.claim.claim_number}"


class SoroScoreLog(models.Model):
    """Log of Soro-Score calculations for audit trail"""
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='score_logs', null=True, blank=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='score_logs', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_logs', null=True, blank=True)
    
    # Score Components
    inconsistency_score = models.FloatField()
    urgency_score = models.FloatField()
    sentiment_score = models.FloatField()
    media_integrity_score = models.FloatField()
    historical_score = models.FloatField()
    
    # Weighted Components
    weighted_inconsistency = models.FloatField()
    weighted_urgency = models.FloatField()
    weighted_sentiment = models.FloatField()
    weighted_media = models.FloatField()
    weighted_historical = models.FloatField()
    
    # Final Score
    final_soro_score = models.FloatField()
    risk_level = models.CharField(max_length=20)
    
    # Metadata
    calculation_metadata = models.JSONField(default=dict)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-calculated_at']
    
    def __str__(self):
        target = self.claim or self.policy or self.user
        return f"Soro-Score Log for {target}"


class Payment(models.Model):
    """Payment records for premiums and claims"""
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')
    
    class PaymentType(models.TextChoices):
        PREMIUM = 'premium', _('Premium Payment')
        CLAIM = 'claim', _('Claim Payment')
        RENEWAL = 'renewal', _('Policy Renewal')
        OTHER = 'other', _('Other')
    
    payment_reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    
    # Payment Details
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    
    # Related Objects
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    # Payment Provider
    payment_gateway = models.CharField(max_length=50)  # paystack, redpay, etc.
    gateway_reference = models.CharField(max_length=200, blank=True, null=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Voice Payment
    voice_payment = models.BooleanField(default=False)
    voice_confirmation_file = models.FileField(upload_to='payment_voice/', null=True, blank=True)
    
    # Metadata
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-initiated_at']
    
    def __str__(self):
        return f"Payment {self.payment_reference} - {self.get_payment_type_display()}"


class Notification(models.Model):
    """Notifications for users"""
    
    class NotificationType(models.TextChoices):
        VOICE = 'voice', _('Voice Notification')
        SMS = 'sms', _('SMS')
        EMAIL = 'email', _('Email')
        PUSH = 'push', _('Push Notification')
        WHATSAPP = 'whatsapp', _('WhatsApp')
    
    class NotificationStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENT = 'sent', _('Sent')
        DELIVERED = 'delivered', _('Delivered')
        FAILED = 'failed', _('Failed')
        READ = 'read', _('Read')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Notification Details
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # For voice notifications
    voice_file = models.FileField(upload_to='notifications/voice/', null=True, blank=True)
    voice_message = models.TextField(blank=True, null=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=NotificationStatus.choices, default=NotificationStatus.PENDING)
    
    # Related Objects
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True, blank=True)
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.user.phone_number}: {self.title}"


class AdminDashboard(models.Model):
    """Admin dashboard settings and cached data"""
    
    class DashboardType(models.TextChoices):
        RISK_HEATMAP = 'risk_heatmap', _('Risk Heatmap')
        CLAIMS_OVERVIEW = 'claims_overview', _('Claims Overview')
        REVENUE = 'revenue', _('Revenue Dashboard')
        USER_ANALYTICS = 'user_analytics', _('User Analytics')
    
    dashboard_type = models.CharField(max_length=50, choices=DashboardType.choices, unique=True)
    data = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)
    refresh_interval = models.IntegerField(default=300)  # seconds
    
    def __str__(self):
        return f"{self.get_dashboard_type_display()} Dashboard"
    
    @classmethod
    def get_or_create_dashboard(cls, dashboard_type):
        dashboard, created = cls.objects.get_or_create(dashboard_type=dashboard_type)
        return dashboard