from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow frontend to interact with backend

# Create table if not exists
def init_db():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

init_db()

# Helper to fetch all tasks
def get_all_tasks():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, completed FROM tasks")
        rows = cursor.fetchall()
        return [{"id": r[0], "title": r[1], "completed": bool(r[2])} for r in rows]

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(get_all_tasks())

# POST create task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (data['title'], False))
        conn.commit()
        task_id = cursor.lastrowid

    return jsonify({'id': task_id, 'title': data['title'], 'completed': False}), 201

# PUT update task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    if not data or 'title' not in data or 'completed' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ?, completed = ? WHERE id = ?", (data['title'], data['completed'], task_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        conn.commit()

    return jsonify({'id': task_id, 'title': data['title'], 'completed': data['completed']})

# DELETE task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        conn.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
