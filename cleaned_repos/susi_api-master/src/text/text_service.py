import requests
from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource

api = Namespace("api/text", description="text operations")


@api.route("/chat/completions", methods=["POST"])
class ChatCompletion(Resource):
    @api.doc("chat_completions")
    def post(self):
        openai_api_key = current_app.config["OPENAI_API_KEY"]
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"})

        messages = data.get("messages")
        if not messages:
            return jsonify({"error": "No messages provided"})

        if not openai_api_key:
            return jsonify({"error": "No OpenAI API key provided"})

        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "messages": messages,
            "model": "gpt-3.5-turbo",
            "temperature": 1.0,
            "max_tokens": 50,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        return jsonify(response.json())
