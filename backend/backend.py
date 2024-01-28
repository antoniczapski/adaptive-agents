from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    if not data:
        return jsonify(error='No JSON object provided'), 400
    if 'conversationHistory' not in data:
        return jsonify(error='No conversationHistory field in JSON object'), 400
    conversationHistory = data['conversationHistory']
    if not conversationHistory:
        return jsonify(error='Empty conversation history'), 400
    # Get the last message from the user
    lastUserMessage = next((message for message in reversed(conversationHistory) if message['sender'] == 'User'), None)
    if not lastUserMessage:
        return jsonify(error='No user message in conversation history'), 400
    message = lastUserMessage['message']
    return jsonify(message=message.upper())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)