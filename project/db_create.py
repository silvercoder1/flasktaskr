from views import db
from models import Task
from datetime import date

#create the database and the tables
db.create_all()

# insert data
#db.session.add(Task("Finish this tute", date(2015, 5, 12), 10, 1))
#db.session.add(Task("Be iOS champ", date(2015, 11, 14), 7, 1))

#commit changes
db.session.commit()



