from datetime import datetime
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g, Blueprint
from .forms import AddTaskForm
from project import db
from project.models import Task, User

################
#### config ####
################

tasks_blueprint = Blueprint('tasks', __name__)

################
#### helper functions ####
################

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('users.login'))
	return wrap


def open_tasks():
	return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())

def closed_tasks():
	return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())


################
#### routes ####
################

@tasks_blueprint.route('/tasks/')
@login_required
def tasks():

	#implement using sqlalchemy
	#open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	#open_tasks = Task.query.filter_by(status='1').order_by(Task.due_date.asc())
	#closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

	userId = User.query.filter_by(id=session['user_id']).first()
	return render_template('tasks.html',form = AddTaskForm(request.form),
	 open_tasks = open_tasks(), closed_tasks=closed_tasks(), username = session['name'])


#add new task
@tasks_blueprint.route('/add/', methods=['GET','POST'])
@login_required
def new_task():

	#implement using sqlalchemy and flask-wtforms
	error = None
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(form.name.data, form.due_date.data, form.priority.data, datetime.utcnow(), '1', session['user_id'])
			db.session.add(new_task)
			db.session.commit()
			flash('New task was successfully posted')
			return redirect(url_for('tasks.tasks'))
		else:
			return render_template('tasks.html', form=form, error=error, open_tasks = open_tasks(), closed_tasks=closed_tasks())


#mark task as completed
@tasks_blueprint.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	
	#implement using sqlalchemy
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	#db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
	if task.first().user_id == session["user_id"] or session['role'] == "admin":
		task.update({"status":"0"})
		db.session.commit()
		flash('The task was marked as completed')
		return redirect(url_for('tasks.tasks'))

	else:
		flash('You can only update tasks that belong to you.')
		return redirect(url_for('tasks.tasks'))


#delete a task
@tasks_blueprint.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	
	#implement using sqlalchemy
	new_id = task_id
	#db.session.query(Task).filter_by(task_id=new_id).delete()
	task = db.session.query(Task).filter_by(task_id=new_id)
	if task.first().user_id == session["user_id"] or session['role'] == "admin":
		task.delete()
		db.session.commit()
		flash('the task was deleted')
		return redirect(url_for('tasks.tasks'))
	else:
		flash("you can only delete tasks that you've created")
		return redirect(url_for('tasks.tasks'))


