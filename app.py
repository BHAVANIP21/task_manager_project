from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory data store
tasks = []
next_id = 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()

    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": next_id,
        "title": data['title'].strip(),
        "completed": False
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['completed'] = data.get('completed', task['completed'])
            return jsonify({"message": "Task updated"}), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

