from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, default=False)

    # Representación
    def __init__(self,name,status):
        self.name=name
        self.status=status

    def to_json(self):
        return{
            "id":self.id,
            "name":self.name,
            "status":self.status
        }
    
    def __repr__(self):
        return f'<Task {self.name}>'

# Table Plus
@app.route('/')
def index():
    return 'Welcome to my ORM app'

@app.route('/create')
def create_tables():
    db.create_all()
    return "Tables created..."

@app.route('/new',methods=["POST"])
def create_task():
    if not request.json or 'name' not in request.json:
        abort(400)
    task = Task(name=request.json["name"],status=False)  
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json()),201

@app.route('/tasks',methods=["GET"])
def read():
    tasks = Task.query.all()
    return jsonify([task.to_json() for task in tasks])

@app.route('/tasks/<id>',methods=["PUT"])
def update(id):
    task=Task.query.get(id)
    if not task:
        return "Task not found"
    task.status=not task.status
    db.session.commit()
    return "Task updated"

@app.route('/delete/<id>',methods=["DELETE"])
def delete(id):
    task=Task.query.get_or_404(id)
    db.session.delete(task)    
    db.session.commit()
    return jsonify({"status":"True"}),201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


