from users.serializers import UserSerializer
from rest_framework import serializers
from .models import Conversation, Message, Room


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('conversation',) 


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()
    receiver = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        last_message = instance.messages.first() 
        if last_message:
            return MessageSerializer(instance=last_message).data
        return None


class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()
    receiver = UserSerializer()
    messages = MessageSerializer(many=True)  # Adjusted to match the model change

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'messages']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

