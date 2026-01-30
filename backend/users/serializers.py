from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, UserActivity


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = (
            'phone_number', 'email', 'first_name', 'last_name',
            'password', 'password2', 'user_type', 'date_of_birth'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                              phone_number=phone_number, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "phone_number" and "password".')
        
        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    risk_level = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email', 'first_name', 'last_name',
            'user_type', 'date_of_birth', 'bvn', 'nin', 'address',
            'state', 'lga', 'soro_score', 'risk_level',
            'total_claims', 'approved_claims', 'rejected_claims',
            'bank_account_number', 'bank_name', 'account_name',
            'prefers_voice', 'whatsapp_number', 'profile',
            'created_at', 'updated_at'
        )
        read_only_fields = ('soro_score', 'total_claims', 'approved_claims', 
                          'rejected_claims', 'created_at', 'updated_at')


class UserActivitySerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value