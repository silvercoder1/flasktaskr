import os
import unittest
from datetime import date

import json

from project import app, db
from project._config import basedir
from project.models import Task

TEST_DB = "test.db"

class APITests(unittest.TestCase):

	#setup and teardown

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)

		self.app = app.test_client()
		db.create_all()

		self.assertEquals(app.debug, False)

	def tearDown(self):
		db.session.remove()
		db.drop_all()


	#helper methods

	def add_tasks(self):

		db.session.add(Task("Run around in circles", date(2016, 10, 22), 10, date(2015, 10, 22), 1, 1))
		db.session.commit()

		db.session.add(Task("Purchase Real Python", date(2016, 10, 12), 10, date(2015, 10, 22), 1, 1))
		db.session.commit()

	#tests

	def test_collection_endpoint_returns_correct_data(self):
		self.add_tasks()
		response = self.app.get('api/v1/tasks/', follow_redirects = True)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.mimetype, 'application/json')
		self.assertIn(b'Run around in circles', response.data)
		self.assertIn(b'Purchase Real Python', response.data)

	def test_task_endpoint_returns_correct_data(self):
		self.add_tasks()
		response = self.app.get('api/v1/tasks/1/', follow_redirects = True)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.mimetype, 'application/json')
		self.assertIn(b'Run around in circles', str(response.data))
		self.assertNotIn(b'Purchase Real Python', str(response.data))

	def test_invalid_task_endpoint_returns_error(self):
		self.add_tasks()
		response = self.app.get('api/v1/tasks/10/', follow_redirects = True)

		self.assertEquals(response.status_code, 404)
		self.assertEquals(response.mimetype, 'application/json')
		self.assertIn(b'element does not exist', str(response.data))

	def test_new_task_successfully_posted(self):
		get_response = self.app.get('api/v1/newtask/', follow_redirects = True)
		self.assertEquals(get_response.status_code, 200)

		self.assertIn(b'error', str(get_response.data))

		post_response = self.app.post('api/v1/newtask/', data=json.dumps({'testonly': 'ok lah'}), follow_redirects = True)
		self.assertEquals(post_response.status_code, 200)
		self.assertIn(b'You have added', str(post_response.data))



if __name__ == "__main__":
	unittest.main()

