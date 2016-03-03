from functools import wraps
from flask import flash, redirect, jsonify, \
session, url_for, Blueprint, make_response, request

from project import db
from project.models import Task
import json

import datetime


#config

api_blueprint = Blueprint('api', __name__)


#helper functions

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('users.login'))
	return wrap


def open_tasks():
	return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
	return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())


#routes

@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
	results = db.session.query(Task).limit(10).offset(0).all()
	json_results = []

	for result in results:
		data = {
		'task_id':result.task_id,
		'task name':result.name,
		'due date':unicode(result.due_date),
		'priority': result.priority,
		'posted date': unicode(result.posted_date),
		'status': result.status,
		'user id': result.user_id
		}
		json_results.append(data)

	return jsonify(items=json_results)

@api_blueprint.route('/api/v1/tasks/<int:task_id>/')
def get_task(task_id):
	result = db.session.query(Task).filter_by(task_id=task_id).first()
	code = ''
	if result:

		data = {
			'task_id':result.task_id,
			'task name':result.name,
			'due date':unicode(result.due_date),
			'priority': result.priority,
			'posted date': unicode(result.posted_date),
			'status': result.status,
			'user id': result.user_id
			}
		code = 200
	else:
		data = {'error': 'element does not exist'}
		code = 404
	
	return make_response(jsonify(data), code)


@api_blueprint.route('/api/v1/newtask/', methods = ['GET', 'POST'])
def new_task():
	data_dic = {}
	code = ''
	if request.method == 'POST':

		req_data = json.loads(request.data)
		req_dict = dict(req_data)
		keys = req_dict.keys()

		if not req_data['name'] or not req_data['due_date'] \
		or not req_data['priority'] or not req_data['posted_date'] \
		or not req_data['status'] or not req_data['user_id']:

			data_dic = {'error': 'invalid data sent'}
			code = 404
		else:
			
			task = Task(req_data['name'], datetime.datetime.strptime(req_data['due_date'], "%m/%d/%Y"), req_data['priority'], 
				datetime.datetime.strptime(req_data['posted_date'], "%m/%d/%Y"), req_data['status'], req_data['user_id'])
			db.session.add(task)
			db.session.commit()
			data_dic = {'success': 'task is properly posted'}
			code = 200

	else:
		data_dic = {'error': 'post only'}
		code = 400

	return make_response(jsonify(items=data_dic), code)


@api_blueprint.route('/api/v1/delete_task/<int:task_id>/', methods = ['GET', 'POST'])
def delete_task(task_id):
	data_dic = {}
	code = ''
	if request.method == 'POST':
		task = db.session.query(Task).filter_by(task_id=task_id)
		if task:
			task.delete()
			db.session.commit()
			data_dic = {'success': 'task {} is properly DELETED'.format(task_id)}
			code = 200
		else:
			data_dic = {'error': 'task {} is not found'.format(task_id)}
			code = 200

		
	else:
		data_dic = {'error': 'post only'}
		code = 400

	return make_response(jsonify(items=data_dic), code)


@api_blueprint.route('/api/v1/update_task/<int:task_id>/', methods = ['GET', 'POST'])
def update_task(task_id):
	data_dic = {}
	code = ''

	if request.method == 'POST':
		req_data = json.loads(request.data)
		
		req_dict = dict(req_data)
		keys = req_dict.keys()
		task = db.session.query(Task).filter_by(task_id=task_id)
		if 'name' in keys:
			task.update({"name": req_data['name']})
		if 'due_date' in keys:
			task.update({"due_date": datetime.datetime.strptime(req_data['due_date'], "%m/%d/%Y")})
		if 'priority' in keys:
			task.update({"priority": req_data['priority']})
		if 'staus' in keys:
			task.update({"status": req_data['status']})

		db.session.commit()
		data_dic = {'success': 'task {} UPDATED'.format(task_id)}
		code = 200

		

		
	else:
		data_dic = {'error': 'post only'}
		code = 400
	return make_response(jsonify(items=data_dic), code)





