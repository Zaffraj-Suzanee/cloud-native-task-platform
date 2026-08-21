from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///tasks.db"
)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)


# Task database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="pending")


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


# GET all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    return jsonify([
        {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }
        for task in tasks
    ])


# POST create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "Title is required"
        }), 400

    task = Task(
        title=data["title"],
        status=data.get("status", "pending")
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "status": task.status
    }), 201


# PUT update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    data = request.get_json() or {}

    if "title" in data:
        task.title = data["title"]

    if "status" in data:
        task.status = data["status"]

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "status": task.status
    })


# DELETE a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    })


# Create database tables
with app.app_context():
    db.create_all()


# Run application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
