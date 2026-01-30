from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    InsuranceProduct, Policy, Claim, VoiceAnalysis,
    SoroScoreLog, Payment, Notification, AdminDashboard
)

User = get_user_model()


class InsuranceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProduct
        fields = '__all__'


class PolicySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Policy
        fields = '__all__'
        read_only_fields = ('policy_number', 'created_at', 'updated_at')


class VoiceAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceAnalysis
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    policy_number = serializers.CharField(source='policy.policy_number', read_only=True)
    voice_analysis = VoiceAnalysisSerializer(read_only=True)
    
    # For voice recording
    audio_file = serializers.FileField(write_only=True, required=False)
    
    class Meta:
        model = Claim
        fields = '__all__'
        read_only_fields = (
            'claim_number', 'soro_score', 'risk_level', 'sentiment_score',
            'urgency_score', 'inconsistency_score', 'keywords',
            'auto_approval_recommended', 'reviewed_by', 'reviewed_at',
            'paid_at', 'submitted_at', 'created_at', 'updated_at'
        )
    
    def create(self, validated_data):
        audio_file = validated_data.pop('audio_file', None)
        claim = Claim.objects.create(**validated_data)
        
        if audio_file:
            claim.audio_file = audio_file
            claim.save()
        
        return claim


class SoroScoreLogSerializer(serializers.ModelSerializer):
    target_type = serializers.SerializerMethodField()
    target_identifier = serializers.SerializerMethodField()
    
    class Meta:
        model = SoroScoreLog
        fields = '__all__'
    
    def get_target_type(self, obj):
        if obj.claim:
            return 'claim'
        elif obj.policy:
            return 'policy'
        elif obj.user:
            return 'user'
        return None
    
    def get_target_identifier(self, obj):
        if obj.claim:
            return obj.claim.claim_number
        elif obj.policy:
            return obj.policy.policy_number
        elif obj.user:
            return obj.user.phone_number
        return None


class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_reference', 'initiated_at', 'completed_at', 'updated_at')


class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at', 'delivered_at', 'read_at')


class AdminDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDashboard
        fields = '__all__'
        read_only_fields = ('last_updated',)


# Specialized serializers for specific operations
class VoiceClaimSerializer(serializers.Serializer):
    """Serializer for voice claim submission"""
    policy_id = serializers.IntegerField(required=True)
    claim_type = serializers.CharField(max_length=50, required=True)
    incident_date = serializers.DateField(required=True)
    incident_location = serializers.CharField(max_length=500, required=True)
    estimated_loss = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    audio_file = serializers.FileField(required=True)
    photos = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        default=list
    )
    description = serializers.CharField(required=False, allow_blank=True)


class UnderwritingResultSerializer(serializers.Serializer):
    """Serializer for underwriting results"""
    soro_score = serializers.FloatField()
    risk_level = serializers.CharField()
    auto_approval_recommended = serializers.BooleanField()
    confidence = serializers.FloatField()
    components = serializers.DictField()
    flags = serializers.ListField(child=serializers.CharField())
    recommendation = serializers.CharField()


class PaymentInitiationSerializer(serializers.Serializer):
    """Serializer for payment initiation"""
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    currency = serializers.CharField(default='NGN')
    payment_type = serializers.CharField(required=True)
    policy_id = serializers.IntegerField(required=False)
    claim_id = serializers.IntegerField(required=False)
    voice_confirmation = serializers.FileField(required=False)
    
    def validate(self, data):
        payment_type = data.get('payment_type')
        policy_id = data.get('policy_id')
        claim_id = data.get('claim_id')
        
        if payment_type == 'premium' and not policy_id:
            raise serializers.ValidationError("policy_id is required for premium payments")
        
        if payment_type == 'claim' and not claim_id:
            raise serializers.ValidationError("claim_id is required for claim payments")
        
        return data


class USSDRequestSerializer(serializers.Serializer):
    """Serializer for USSD requests"""
    session_id = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    service_code = serializers.CharField(required=True)
    text = serializers.CharField(required=True)