from _config import DATABASE_PATH
import sqlite3

with sqlite3.connect(DATABASE_PATH) as connection:
	c = connection.cursor()
	c.execute('DROP TABLE IF EXISTS tasks')
	c.execute("""CREATE Table tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, 
		due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)""")


	#populate with dummy data
	c.execute("""INSERT INTO tasks(name, due_date, priority, status) 
		VALUES('Finish tutorial', '01/10/2015', 10, 1)""")

	c.execute("""INSERT INTO tasks(name, due_date, priority, status) 
		VALUES('Finish courses all', '05/10/2015', 8, 1)""")



