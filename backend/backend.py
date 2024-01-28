from flask import Flask, request, jsonify
from flask_cors import CORS

from database_handling import process_query

app = Flask(__name__)
CORS(app)

# Logging
# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Body: %s', request.get_data())

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    if not data:
        return jsonify(error='No JSON object provided'), 400
    if 'prompt' not in data:
        return jsonify(error='No prompt field in JSON object'), 400
    prompt = data['prompt']
    if not prompt:
        return jsonify(error='Empty prompt'), 400
    return jsonify(message=process_query(prompt))

if __name__ == '__main__':
    # backend
    app.run(host='0.0.0.0', port=5001, debug=True)