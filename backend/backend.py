from flask import Flask, request, jsonify
from flask_cors import CORS

from database import process_query

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
    return jsonify(message=process_query(conversationHistory))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)