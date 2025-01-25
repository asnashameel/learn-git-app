from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for tasks
tasks = {}

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    task_id = len(tasks) + 1
    tasks[task_id] = {
        "title": data["title"],
        "description": data["description"],
        "completed": False  # New field
    }
    return jsonify({"message": "Task created", "task": tasks[task_id]}), 201

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        return jsonify({"message": "Task marked as completed", "task": tasks[task_id]})
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if "title" not in data or "description" not in data:
        return jsonify({"error": "Title and description are required"}), 400
    task_id = len(tasks) + 1
    tasks[task_id] = {
        "title": data["title"],
        "description": data["description"],
        "completed": False
    }
    return jsonify({"message": "Task created", "task": tasks[task_id]}), 201
