import json
import uuid

tasks_db = []

class MockTable:
    def put_item(self, Item):
        tasks_db.append(Item)

    def scan(self):
        return {"Items": tasks_db}

    def delete_item(self, Key):
        global tasks_db
        tasks_db = [task for task in tasks_db if task["id"] != Key["id"]]

table = MockTable()

def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": body
    }

def get_body(event):
    body = event.get("body")
    if not body:
        return {}
    if isinstance(body, str):
        return json.loads(body)
    return body

def lambda_handler(event, context):
    http_method = event.get("requestContext", {}).get("http", {}).get("method")
    raw_path = event.get("rawPath", "")

    try:
        if http_method == "POST" and raw_path == "/tasks":
            body = get_body(event)
            title = body.get("title")

            if not title:
                return response(400, {"error": "title is required"})

            item = {
                "id": str(uuid.uuid4()),
                "title": title,
                "completed": False,
            }

            table.put_item(Item=item)
            return response(201, item)

        elif http_method == "GET" and raw_path == "/tasks":
            result = table.scan()
            return response(200, result["Items"])

        elif http_method == "DELETE" and raw_path.startswith("/tasks/"):
            task_id = raw_path.split("/")[-1]
            table.delete_item(Key={"id": task_id})
            return response(200, {"message": f"Deleted task {task_id}"})

        else:
            return response(404, {"error": "Route not found"})

    except Exception as e:
        return response(500, {"error": str(e)})