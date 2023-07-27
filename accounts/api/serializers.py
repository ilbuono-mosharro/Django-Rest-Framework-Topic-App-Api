from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"}, )
    class Meta:
        model = User
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate_username(self, attrs):
        """
        This method checks if the username is present in the database and is not case-sensitive.
        """
        if User.objects.filter(username__iexact=attrs).exists():
            raise serializers.ValidationError("That username is already taken.")
        return attrs

    def validate_email(self, attrs):
        """
        This method checks if the email is present in the database and is not case-sensitive.
        """
        if User.objects.filter(email__iexact=attrs).exists():
            raise serializers.ValidationError(
                "This email is already registered on our platform, please use another one or "
                "if you have forgotten your password, ask for a new one."
            )
        return attrs

    def validate(self, attrs):
        """
        This method checks if password and password1 are the same.
        """
        password = attrs.get('password')
        password1 = attrs.pop('password1', None)
        if password != password1:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        """
        We are overriding the create method, to set the password for a user securely.
        """
        user = User(**validated_data)
        password = validated_data.pop('password')
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        We are overriding the update method, to choose which fields we want to update.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['username', 'email']


    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']
        read_only_fields = ['first_name', 'last_name', 'avatar']