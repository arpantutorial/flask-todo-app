from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Using a new db name to automatically create the updated schema with 'priority'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///taskflow.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    priority = db.Column(db.String(20), default="Medium")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        priority = request.form.get('priority', 'Medium')
        new_task = Task(title=title, desc=desc, priority=priority)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")
        
    all_tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template('index.html', all_tasks=all_tasks)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    task = Task.query.filter_by(sno=sno).first_or_404()
    if request.method == 'POST':
        task.title = request.form['title']
        task.desc = request.form['desc']
        task.priority = request.form.get('priority', 'Medium')
        db.session.commit()
        return redirect("/")
        
    return render_template('update.html', task=task)

@app.route('/delete/<int:sno>')
def delete(sno):
    task = Task.query.filter_by(sno=sno).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)