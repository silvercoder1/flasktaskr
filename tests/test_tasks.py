from test import *

class TasksTest(AllTests):

	#each test should start with 'test'

	def create_task(self):
		return self.app.post('add/', data=dict(name='go to bank',
			due_date = '02/05/2014',
			priority='1',
			posted_date='02/04/2014',
			status='1'), follow_redirects=True)


	def test_users_can_add_tasks(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		response = self.create_task()
		self.assertIn(b'New task', response.data)

	def test_users_cannot_add_tasks_when_error(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.post('add/', data=dict(name='go to bank',
			due_date = '',
			priority='1',
			posted_date='02/04/2014',
			status='1'), follow_redirects=True)

		self.assertIn(b'is required', response.data)

	def test_user_can_complete_tasks(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertIn(b'marked as completed', response.data)

	def test_user_can_delete_tasks(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('delete/1/', follow_redirects=True)
		self.assertIn(b'was deleted', response.data)

	def test_users_cannot_complete_tasks_not_created_by_them(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()

		self.create_user('vikrambro', 'vbbb@vvv.com','vikramba')
		self.login('vikrambro', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertNotIn(b'marked as completed', response.data)
		self.assertIn(b'can only update tasks', response.data)

	def test_users_cannot_delete_tasks_not_created_by_them(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user('vikrambro', 'vbbb@vvv.com','vikramba')
		self.login('vikrambro', 'vikramba')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get('delete/1/', follow_redirects=True)
		self.assertNotIn(b'the task was deleted', response.data)
		self.assertIn(b"can only delete tasks", response.data)

	def test_admin_users_can_complete_tasks_not_created_by_them(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()

		self.create_admin_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		

		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertNotIn(b"completed", response.data)

	def test_admin_users_can_delete_tasks_not_created_by_them(self):
		self.create_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()

		self.create_admin_user_and_login()
		self.app.get('tasks/', follow_redirects=True)
		

		response = self.app.get('delete/1/', follow_redirects=True)
		self.assertNotIn(b"can only delete tasks", response.data)

	def test_users_cannot_see_modify_link_for_tasks_not_created_by_them(self):
		self.register("vango22", "v22@b.com", "dog1234", "dog1234")
		self.login("vango22", "dog1234")
		self.app.get('tasks/',follow_redirects=True)
		self.create_task()
		self.logout()

		self.register("vango", "v@b.com", "dog1234", "dog1234")
		response = self.login("vango", "dog1234")
		self.app.get('tasks/',follow_redirects=True)
		self.assertNotIn(b'Delete', response.data)
		self.assertNotIn(b'Mark as Complete', response.data)

	def test_users_can_see_modify_link_for_tasks_created_by_them(self):
		self.register("vango22", "v22@b.com", "dog1234", "dog1234")
		self.login("vango22", "dog1234")
		self.app.get('tasks/',follow_redirects=True)
		self.create_task()
		self.logout()

		self.register("vango", "v@b.com", "dog1234", "dog1234")
		self.login("vango", "dog1234")
		self.app.get('tasks/',follow_redirects=True)
		response = self.create_task()
		
		self.assertNotIn(b'complete/2/', response.data)
		self.assertNotIn(b'delete/2/', response.data)

		

	def create_admin_user_and_login(self):
		db.session.add(User("admin_dog", "a@a.com",bcrypt.generate_password_hash("adminbitch"),"admin"))
		db.session.commit()

		self.login("admin_dog", "abs12342")








if __name__ == '__main__':
	unittest.main()