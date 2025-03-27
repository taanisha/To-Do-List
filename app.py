from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    description=db.Column(db.String(300),nullable=True)
    priority=db.Column(db.Integer,nullable=False)

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.priority).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('content')
    description_content = request.form.get('description')
    priority_content  = request.form.get('priority')
    if task_content:
        new_task = Task(content=task_content,description=description_content,priority=priority_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():  # Ensures we are inside an application context
        db.create_all() 
   
    app.run(debug=True)
