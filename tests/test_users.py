from test import *

class UsersTest(AllTests):

	def test_users_can_register(self):
		self.create_user(self.username, self.email, self.password)
		all_users = db.session.query(User).all()
		for user in all_users:
			user.name
		assert user.name == self.username

	def test_form_is_present_on_login_page(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'sign in to access your task list', response.data)


	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo', 'bar')
		self.assertIn(b"Invalid", response.data)

	def test_users_can_login(self):
		self.register(self.username, self.email, self.password, self.password)
		response = self.login(self.username, self.password)
		self.assertIn(b'Welcome', response.data)

	def test_invalid_form_data(self):
		self.register(self.username, self.email, self.password, self.password)
		response = self.login("alert('dadasd');", 	"rags1234")
		self.assertIn(b'Invalid', response.data)

	def test_form_is_present_on_register_page(self):
		response = self.app.get('register/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please register', response.data)

	def test_user_registration(self):
		self.app.get('register/', follow_redirects=True)
		response = self.register(self.username, self.email, self.password, self.password)
		self.assertIn('Thanks for', response.data)

	def test_user_registration_error(self):
		self.app.get('register/', follow_redirects=True)
		self.register(self.username, self.email, self.password, self.password)
		self.app.get('register/', follow_redirects=True)
		response = self.register(self.username, self.email, self.password, self.password)
		self.assertIn(b'already exist', response.data)

	def test_logged_in_users_can_logout(self):
		self.register(self.username, self.email, self.password, self.password)
		self.login(self.username, self.password)
		response = self.logout()
		self.assertIn(b'goodbye', response.data)

	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		self.assertNotIn(b'goodbye', response.data)

	def test_logged_in_users_can_access_tasks_page(self):
		self.register(self.username, self.email, self.password, self.password)
		self.login(self.username, self.password)
		response = self.app.get('tasks/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Add', response.data)

	def test_not_logged_in_users_cannot_access_tasks(self):
		response = self.app.get('tasks/', follow_redirects=True)
		self.assertIn(b'You need to', response.data)

	def test_default_user_role(self):
		db.session.add(User('vikram', "v@vik.com", "ragabo123"))
		db.session.commit()

		users = db.session.query(User).all()
		for user in users:
			self.assertEqual(user.role, "user")

	def test_username_displayed_on_tasks_template(self):
		self.create_user_and_login()
		response = self.app.get('tasks/')
		self.assertIn(self.username, response.data)


if __name__ == '__main__':
	unittest.main()

