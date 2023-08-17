import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Task

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)
Migrate(app, db) # flask db init, flask db migrate, flask db upgrade
CORS(app)

@app.route('/')
def main():
    return jsonify({ "message": "Mi primera app con flask y base de datos"})


@app.route('/todos', methods=['GET'])
def listar_todos():
    todos = Task.query.all() # SELECT * FROM todos; [<Task 1>, <Task 2>]
    todos = list(map(lambda task: task.serialize(), todos))
    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def crear_task():
    body = request.get_json()
    
    task = Task()
    task.label = body["label"]
    
    if 'done' in body:
        task.done = body["done"]
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.serialize()), 201


if __name__ == '__main__':
    app.run()