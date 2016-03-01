from project import db
#from project.models import Task, User
#from datetime import date

#create the database and the tables
db.create_all()

# insert data
'''db.session.add(User("vikrama", "v@vbr.com", "viki1234"))
db.session.add(Task("Finish thisss tute", date(2015, 5, 12), 10, date(2015, 5, 10), 1, 1))
db.session.add(Task("Be iOSss champ", date(2015, 11, 14), 7, date(2015, 5, 10), 1, 1))'''

#commit changes
db.session.commit()



