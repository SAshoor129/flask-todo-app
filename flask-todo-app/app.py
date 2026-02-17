from flask import Flask, render_template, request, redirect, jsonify
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

# Subtask model
class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'title': self.title,
            'is_done': self.is_done,
            'order': self.order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

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
    
    # Relationship to subtasks
    subtasks = db.relationship('Subtask', backref='task', lazy=True, cascade='all, delete-orphan',
                              order_by='Subtask.order')
    
    def is_overdue(self):
        if self.due_date and not self.completed:
            return self.due_date < datetime.utcnow()
        return False
    
    def days_until_due(self):
        if self.due_date:
            delta = self.due_date - datetime.utcnow()
            return delta.days
        return None
    
    def get_completion_percentage(self):
        """Calculate task completion based on subtasks"""
        if not self.subtasks:
            return 100 if self.completed else 0
        done_count = sum(1 for st in self.subtasks if st.is_done)
        return int((done_count / len(self.subtasks)) * 100)

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

# Subtask routes
@app.route("/task/<int:task_id>/subtask/add", methods=["POST"])
def add_subtask(task_id):
    """Add a subtask to a task"""
    task = Task.query.get_or_404(task_id)
    
    if request.is_json:
        data = request.get_json()
        title = data.get("title", "").strip()
    else:
        title = request.form.get("title", "").strip()
    
    if not title or len(title) > 200:
        return jsonify({"error": "Subtask title required (max 200 chars)"}), 400
    
    # Get max order
    max_order = db.session.query(db.func.max(Subtask.order)).filter_by(task_id=task_id).scalar() or 0
    
    subtask = Subtask(task_id=task_id, title=title, order=max_order + 1)
    db.session.add(subtask)
    db.session.commit()
    
    if request.is_json:
        return jsonify(subtask.to_dict()), 201
    else:
        return redirect(f"/task/{task_id}")

@app.route("/subtask/<int:subtask_id>/toggle", methods=["POST"])
def toggle_subtask(subtask_id):
    """Toggle subtask completion status"""
    subtask = Subtask.query.get_or_404(subtask_id)
    subtask.is_done = not subtask.is_done
    db.session.commit()
    
    if request.is_json:
        return jsonify(subtask.to_dict()), 200
    else:
        return redirect(f"/task/{subtask.task_id}")

@app.route("/subtask/<int:subtask_id>/delete", methods=["POST"])
def delete_subtask(subtask_id):
    """Delete a subtask"""
    subtask = Subtask.query.get_or_404(subtask_id)
    task_id = subtask.task_id
    
    db.session.delete(subtask)
    db.session.commit()
    
    if request.is_json:
        return jsonify({"success": True}), 200
    else:
        return redirect(f"/task/{task_id}")

@app.route("/task/<int:task_id>/subtasks", methods=["GET"])
def get_subtasks(task_id):
    """Get all subtasks for a task"""
    task = Task.query.get_or_404(task_id)
    subtasks = Subtask.query.filter_by(task_id=task_id).order_by(Subtask.order).all()
    return jsonify({
        'subtasks': [st.to_dict() for st in subtasks],
        'completion_percentage': task.get_completion_percentage()
    })

@app.route("/subtask/<int:subtask_id>/update", methods=["POST"])
def update_subtask(subtask_id):
    """Update a subtask title"""
    subtask = Subtask.query.get_or_404(subtask_id)
    
    if request.is_json:
        data = request.get_json()
        title = data.get("title", "").strip()
    else:
        title = request.form.get("title", "").strip()
    
    if title and len(title) <= 200:
        subtask.title = title
        db.session.commit()
    
    if request.is_json:
        return jsonify(subtask.to_dict()), 200
    else:
        return redirect(f"/task/{subtask.task_id}")

@app.route("/subtask/<int:subtask_id>/reorder", methods=["POST"])
def reorder_subtask(subtask_id):
    """Reorder subtasks"""
    subtask = Subtask.query.get_or_404(subtask_id)
    
    data = request.get_json() if request.is_json else request.form
    new_order = data.get("order", type=int)
    
    if new_order is not None:
        subtask.order = new_order
        db.session.commit()
    
    if request.is_json:
        return jsonify(subtask.to_dict()), 200
    else:
        return redirect(f"/task/{subtask.task_id}")

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
