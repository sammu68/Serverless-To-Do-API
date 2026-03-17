from flask import Flask, request, jsonify
from app import lambda_handler

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Server is running! Use /tasks endpoint"

@app.route("/tasks", methods=["POST"])
def create_task():
    event = {
        "requestContext": {"http": {"method": "POST"}},
        "rawPath": "/tasks",
        "body": request.get_json()
    }
    result = lambda_handler(event, None)
    return jsonify(result["body"]), result["statusCode"]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    event = {
        "requestContext": {"http": {"method": "GET"}},
        "rawPath": "/tasks"
    }
    result = lambda_handler(event, None)
    return jsonify(result["body"]), result["statusCode"]

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    event = {
        "requestContext": {"http": {"method": "DELETE"}},
        "rawPath": f"/tasks/{task_id}"
    }
    result = lambda_handler(event, None)
    return jsonify(result["body"]), result["statusCode"]

if __name__ == "__main__":
    app.run(debug=True)