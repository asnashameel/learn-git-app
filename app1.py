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
hello
