from django.shortcuts import render
import json
import os
import socket
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from itassist.services import conversation
from .sync_utils import sync_json_to_mysql
from core.settings import CONV_JSON_FILE

# Create your views here.

#For Creating a new conversation
# This function creates a new conversation and saves it to a JSON file.
# It generates a unique conversation ID based on the hostname and the current date and time.
# It also initializes the conversation with a default name and an empty message list.
@api_view(['POST'])
def create_conversation(request):
    print("Creating new conversation...")
    conversations = conversation.load_conversations()
    conv_id = conversation.get_next_conversation_id(conversations)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_convo = {
        "conv_id": conv_id,
        "Name": "New Conversation",
        "Date": created_at,
        "messages": []
    }

    conversations.append(new_convo)
    conversation.save_conversations(conversations)

    return Response(new_convo, status=status.HTTP_201_CREATED)

# This function deletes a conversation based on the provided conversation ID.
# It checks if the conversation exists in the JSON file and removes it if found.
@api_view(['DELETE'])
def delete_conversation(request, conv_id):
    conversations = conversation.load_conversations()

    # Check if it exists
    updated_conversations = [conv for conv in conversations if conv["conv_id"] != conv_id]
    if len(updated_conversations) == len(conversations):
        return Response(
            {"detail": f"Conversation with ID '{conv_id}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    conversation.save_conversations(updated_conversations)
    return Response(
        {"detail": f"Conversation '{conv_id}' deleted successfully."},
        status=status.HTTP_204_NO_CONTENT
    )


# This function retrieves all conversations from the JSON file.
# It returns the list of conversations in the response.
@api_view(['GET'])
def get_all_conversations(request):
    conversations = conversation.load_conversations()
    return Response(conversations, status=status.HTTP_200_OK)



# This function updates the conversation data based on the provided conversation ID.
# It allows updating the conversation name and messages.    
# It checks if the conversation exists and updates it accordingly.
# If the conversation is not found, it returns a 404 error.
@api_view(["PUT"])
def update_conversation(request, conv_id):
    result, stat = conversation.update_conversation_data(conv_id, request.data)
    return Response(result, status=stat)


# This function adds a new user message to the specified conversation.
# It generates a unique message ID based on the existing messages in the conversation.
# It also checks if the conversation exists and adds the message to it.
# If the conversation is not found, it returns a 404 error.
# If the message content is empty, it returns a 400 error.
@api_view(["POST"])
def add_user_message_to_conversation(request, conv_id):
    message_text = request.data.get("message")
    result, status = conversation.add_user_message(conv_id, message_text)
    return Response(result, status=status)


# This function retrieves the details of a specific conversation based on its ID.
# It returns the conversation details if found, or an error message if not found.
# It also includes the messages associated with the conversation.
@api_view(["GET"])
def get_conversation_detail_view(request, conv_id):
    result, status_code = conversation.get_conversation_by_id(conv_id)
    return Response(result, status=status_code)

@api_view(["GET"])
def sync_data_sql_server(request):
    try:
        sync_json_to_mysql()
        return Response({"message": "Data synced successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)