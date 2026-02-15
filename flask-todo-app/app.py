from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Home page
@app.route("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route("/add", methods=["POST"])
def add():
    task_name = request.form["task"]
    new_task = Task(name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

# Complete task
@app.route("/complete/<int:id>")
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect("/")

# Delete task
@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

# Edit task page
@app.route("/edit/<int:id>")
def edit(id):
    task = Task.query.get_or_404(id)
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks, editing_task=task)

# Update task
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Task.query.get_or_404(id)
    task.name = request.form["task_name"]
    db.session.commit()
    return redirect("/")

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
