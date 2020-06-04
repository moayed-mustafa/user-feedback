from app import app
from models import connect_db, db, User, Feedback
db.drop_all()
db.create_all()

# create a user:
username = 'user1'
password = 'this is the password user1 has chosen'
first_name = 'first'
last_name= 'user'
email = 'thefirstuser@email.com'
registered_user = User.register(username, password, first_name, last_name, email)
db.session.add(registered_user)
db.session.commit()

# create some feedbacks and associate them with user1

fb1 = Feedback(title='facebook feedback', content='I find FB to be a very dull and not exciting app', username=username)
fb2 = Feedback(title='twitter feedback', content='I find twitter to be a very nice and  exciting app', username=username)
fb3 = Feedback(title='reddit feedback', content='I think reddit is the best thing that happend to the internet', username=username)

db.session.add_all([fb1, fb2, fb3])
db.session.commit()