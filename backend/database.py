from flask import jsonify

def process_query(conversationHistory):
    lastUserMessage = next((message for message in reversed(conversationHistory) if message['sender'] == 'User'), None)
    if not lastUserMessage:
        return jsonify(error='No user message in conversation history'), 400
    message = lastUserMessage['message']
    return message.upper()