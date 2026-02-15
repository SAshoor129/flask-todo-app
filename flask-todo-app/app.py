from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from enum import Enum

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Enums for Task
class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusEnum(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

# Task model with metadata
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default="Medium")
    status = db.Column(db.String(20), default="todo")
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_overdue(self):
        if self.due_date and not self.completed:
            return self.due_date < datetime.utcnow()
        return False
    
    def days_until_due(self):
        if self.due_date:
            delta = self.due_date - datetime.utcnow()
            return delta.days
        return None

# Home page
@app.route("/")
def index():
    search = request.args.get('q', '').strip()
    priority_filter = request.args.get('priority', '').strip()
    status_filter = request.args.get('status', '').strip()
    date_filter = request.args.get('date_filter', '').strip()
    sort_by = request.args.get('sort', 'created_at_desc').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Build query
    query = Task.query
    
    # Apply search filter
    if search:
        query = query.filter(
            db.or_(
                Task.name.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%')
            )
        )
    
    # Apply priority filter
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    
    # Apply status filter
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    # Apply date range filter
    today = datetime.utcnow().date()
    if date_filter == 'overdue':
        query = query.filter(
            Task.due_date < datetime.utcnow(),
            Task.completed == False
        )
    elif date_filter == 'today':
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        query = query.filter(Task.due_date.between(start, end))
    elif date_filter == 'this_week':
        start = today
        end = today + timedelta(days=7)
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.max.time())
        query = query.filter(Task.due_date.between(start_dt, end_dt))
    elif date_filter == 'no_due_date':
        query = query.filter(Task.due_date == None)
    
    # Apply sorting
    if sort_by == 'due_date_asc':
        query = query.order_by(Task.due_date.asc().nullslast())
    elif sort_by == 'due_date_desc':
        query = query.order_by(Task.due_date.desc().nullslast())
    elif sort_by == 'priority_high':
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        query = query.order_by(db.case({p: i for i, p in priority_order.items()}, value=Task.priority))
    elif sort_by == 'priority_low':
        priority_order = {'Low': 1, 'Medium': 2, 'High': 3}
        query = query.order_by(db.case({p: i for i, p in priority_order.items()}, value=Task.priority))
    elif sort_by == 'name_asc':
        query = query.order_by(Task.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Task.name.desc())
    elif sort_by == 'created_at_asc':
        query = query.order_by(Task.created_at.asc())
    else:  # created_at_desc (default)
        query = query.order_by(Task.created_at.desc())
    
    # Pagination
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = paginated.items
    total_pages = paginated.pages
    total_count = paginated.total
    
    # Get stats for dashboard
    all_tasks = Task.query.all()
    overdue_count = sum(1 for t in all_tasks if t.is_overdue())
    
    return render_template("index.html", 
                          tasks=tasks, 
                          search=search,
                          priority_filter=priority_filter,
                          status_filter=status_filter,
                          date_filter=date_filter,
                          sort_by=sort_by,
                          page=page,
                          total_pages=total_pages,
                          total_count=total_count,
                          overdue_count=overdue_count)

# View task details
@app.route("/task/<int:id>")
def view_task(id):
    task = Task.query.get_or_404(id)
    return render_template("task_detail.html", task=task)

# Add task
@app.route("/add", methods=["POST"])
def add():
    task_name = request.form["task"]
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium")
    status = request.form.get("status", "todo")
    due_date_str = request.form.get("due_date", "").strip()
    
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except (ValueError, TypeError):
            due_date = None
    
    new_task = Task(
        name=task_name,
        description=description,
        priority=priority,
        status=status,
        due_date=due_date
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

# Complete task
@app.route("/complete/<int:id>")
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    if task.completed:
        task.status = "done"
    else:
        task.status = "todo"
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect("/")

# Update task status
@app.route("/status/<int:id>/<new_status>")
def update_status(id, new_status):
    task = Task.query.get_or_404(id)
    if new_status in ["todo", "doing", "done"]:
        task.status = new_status
        if new_status == "done":
            task.completed = True
        else:
            task.completed = False
        task.updated_at = datetime.utcnow()
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
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks, editing_task=task)

# Update task
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Task.query.get_or_404(id)
    task.name = request.form.get("task_name", task.name)
    task.description = request.form.get("description", task.description).strip()
    task.priority = request.form.get("priority", task.priority)
    task.status = request.form.get("status", task.status)
    
    due_date_str = request.form.get("due_date", "").strip()
    if due_date_str:
        try:
            task.due_date = datetime.fromisoformat(due_date_str)
        except (ValueError, TypeError):
            pass
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect("/")

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
