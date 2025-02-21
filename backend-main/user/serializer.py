from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not phone or not password:
            raise serializers.ValidationError("Phone and password are required.")

        user = authenticate(request=self.context.get('request'), phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        attrs['user'] = user
        return attrs
    



class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'full_name', 'date_of_birth', 'address', 'email', 
            'password', 'confirm_password', 'citizenship_no', 
            'phone', 'image'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # Validate password and confirm password match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        # Check if the email already exists in the database
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("Email is already in use.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
