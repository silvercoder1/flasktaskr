import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

	#executed prior to each test
	def setUp(self):

		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()


	#executed after each test
	def tearDown(self):

		db.session.remove()
		db.drop_all()

	def login(self, username, password):
		return self.app.post('/', data=dict(username=username, password=password), follow_redirects=True)

	def register(self, name, email, password, confirm):
		return self.app.post('register/', data=dict(name=name, email=email, password=password, confirm=confirm),
			follow_redirects=True)

	def logout(self):
		return self.app.get('logout/', follow_redirects=True)


	def create_user(self, name, email, password):
		new_user = User(name=name, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

	def create_task(self):
		return self.app.post('add/', data=dict(name='go to bank',
			due_date = '02/05/2014',
			priority='1',
			posted_date='02/04/2014',
			status='1'), follow_redirects=True)







	#each test should start with 'test'


	def test_users_can_register(self):
		new_user = User("vikram", "vik@v.com", "viki123456")
		db.session.add(new_user)
		db.session.commit()

		all_users = db.session.query(User).all()
		for user in all_users:
			user.name
		assert user.name == "vikram"

	def test_form_is_present_on_login_page(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'sign in to access your task list', response.data)

	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo', 'bar')
		self.assertIn(b"Invalid", response.data)

	def test_users_can_login(self):
		self.register("vikrambahl", "v@broo.com", "rags1234", "rags1234")
		response = self.login("vikrambahl", "rags1234")
		self.assertIn(b'Welcome', response.data)

	def test_invalid_form_data(self):
		self.register("vikrambahl", "v@broo.com", "rags1234", "rags1234")
		response = self.login("alert('dadasd');", "rags1234")
		self.assertIn(b'Invalid', response.data)

	def test_form_is_present_on_register_page(self):
		response = self.app.get('register/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please register', response.data)

	def test_user_registration(self):
		self.app.get('register/', follow_redirects=True)
		response = self.register("michael1243", "mike@m.com", "mickey", "mickey")
		self.assertIn('Thanks for', response.data)

	def test_user_registration_error(self):
		self.app.get('register/', follow_redirects=True)
		self.register("michael1243", "mike@m.com", "mickey", "mickey")
		self.app.get('register/', follow_redirects=True)
		response = self.register("michael1243", "mike@m.com", "mickey", "mickey")
		self.assertIn(b'already exist', response.data)

	def test_logged_in_users_can_logout(self):
		self.register("raghuram", "r@bbbb.com", "roogaboss", "roogaboss")
		self.login("raghuram", "roogaboss")
		response = self.logout()
		self.assertIn(b'goodbye', response.data)

	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		self.assertNotIn(b'goodbye', response.data)

	def test_logged_in_users_can_access_tasks_page(self):
		self.register('vikrama', 'vikrama@v.com', 'vikic1234', 'vikic1234')
		self.login('vikrama', 'vikic1234')
		response = self.app.get('tasks/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Add', response.data)

	def test_not_logged_in_users_cannot_access_tasks(self):
		response = self.app.get('tasks/', follow_redirects=True)
		self.assertIn(b'You need to', response.data)

	def test_users_can_add_tasks(self):
		self.create_user('vikram', 'v@vvv.com','vikramba')
		self.login('vikram', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		response = self.create_task()
		self.assertIn(b'New task', response.data)

	def test_users_cannot_add_tasks_when_error(self):
		self.create_user('vikram', 'v@vvv.com','vikramba')
		self.login('vikram', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.post('add/', data=dict(name='go to bank',
			due_date = '',
			priority='1',
			posted_date='02/04/2014',
			status='1'), follow_redirects=True)

		self.assertIn(b'is required', response.data)

	def test_user_can_complete_tasks(self):
		self.create_user('vikram', 'v@vvv.com','vikramba')
		self.login('vikram', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertIn(b'marked as completed', response.data)

	def test_user_can_delete_tasks(self):
		self.create_user('vikram', 'v@vvv.com','vikramba')
		self.login('vikram', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('delete/0/', follow_redirects=True)
		self.assertIn(b'was deleted', response.data)

	def test_users_cannot_complete_tasks_not_created_by_them(self):
		self.create_user('vikram', 'v@vvv.com','vikramba')
		self.login('vikram', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()

		self.create_user('vikrambro', 'vbbb@vvv.com','vikramba')
		self.login('vikrambro', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertNotIn(b'marked as completed', response.data)









if __name__ == '__main__':
	unittest.main()