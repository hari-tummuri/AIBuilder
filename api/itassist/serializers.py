from rest_framework import serializers
from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Conversation
        fields = ['conv_id', 'Name', 'Date']

class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.SlugRelatedField(
        queryset=Conversation.objects.using('azure').all(),
        slug_field='conv_id'
    )
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'from_field', 'message', 'time']