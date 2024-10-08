from rest_framework import serializers

from chat.models import CustomUser, Message


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializers for Custom User Model
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'bio', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializers for Message Model
    """
    sender_username = serializers.ReadOnlyField(source='sender.username')
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']