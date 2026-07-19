from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True)
    is_landlord = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_landlord']

    def create(self, validated_data):
        is_landlord = validated_data.pop('is_landlord', False)

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Assign user to a group based on role
        if is_landlord:
            group, _ = Group.objects.get_or_create(name='landlords')
        else:
            group, _ = Group.objects.get_or_create(name='tenants')

        user.groups.add(group)
        return user