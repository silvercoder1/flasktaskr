import os
import unittest
import datetime
from project import app, db, bcrypt
from project._config import basedir
from project.models import User, Task

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

	username = "vikram12"
	email = "v@v.com"
	password = "viki12344"

	#executed prior to each test
	def setUp(self):

		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
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
		new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
		db.session.add(new_user)
		db.session.commit()

	def create_user_and_login(self):
		self.create_user(self.username, self.email, self.password)
		self.login(self.username, self.password)

	#tests

	def test_404_error(self):
		response = self.app.get('/thisDoesntExist/')
		self.assertEquals(response.status_code, 404)
		self.assertIn(b'Sorry. 404.', response.data)

	def test_500_error(self):
		bad_user = User("dogcock", "d@f.com", bcrypt.generate_password_hash("fangorn123"))
		db.session.add(bad_user)
		db.session.commit()
		response = self.login('dogcock', 'fangorn12')
		self.assertNotEquals(response.status_code, 500)
		self.assertNotIn(b'ValueError: Invalid salt', response.data)
		self.assertNotIn(b'Something went terribly wrong.', response.data)

	

