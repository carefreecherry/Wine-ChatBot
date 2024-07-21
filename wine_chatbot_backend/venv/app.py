from flask import Flask, request, jsonify, Response, stream_with_context
from chatbot import get_response_stream
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    def generate():
        for chunk in get_response_stream(query):
            yield chunk

    return Response(stream_with_context(generate()), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)