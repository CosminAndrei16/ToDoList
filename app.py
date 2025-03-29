from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definirea modelului pentru task-uri
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Crearea bazei de date
with app.app_context():
    db.create_all()

# Endpoint pentru obținerea task-urilor
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": todo.id, "text": todo.text, "completed": todo.completed} for todo in todos])

# Endpoint pentru adăugarea unui task nou
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(text=data['text'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

# Endpoint pentru actualizarea unui task (marcare ca finalizat)
@app.route('/todos/<int:id>', methods=['PUT'])
def complete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Task not found"}), 404

    todo.completed = not todo.completed
    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

# Endpoint pentru ștergerea unui task
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
