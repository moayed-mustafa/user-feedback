from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    """ model for creting the users table inside my database """
    __tablename__ = 'users';

    # setup the columns

    username =db.Column(db.String(20),primary_key=True)

    password = db.Column(db.String(100),nullable=False)

    email = db.Column(db.String(40), nullable=False, unique=True)

    first_name = db.Column(db.String(20), nullable=False, unique=False)

    last_name = db.Column(db.String(20), nullable=False, unique=False)


    """Register user w/hashed password & return user."""
    # registration calss method
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user w/hashed and salted password & return user."""
        # hash the password strign the user chosed
        hashed_password = bcrypt.generate_password_hash(password)
        # turn the bytes string to a character string for storing it on the database
        # we do this becaue the database password model is expecting a TEXT, not a Bytes datatype
        hashed_utf8 = hashed_password.decode("utf8")
        # return instance of the user and the hashed password
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name,email=email)
        # end_register
         # registration calss method
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        user = User.query.get(username)
        # check if user existes and the password string matches the hash string associated with the user.
        if user and bcrypt.check_password_hash(user.password, password):
            return user

        else:
            return False

        # end_authentication

    # create a feedback model
class Feedback(db.Model):
    """ a feedback models to associate feedback posts with users """
    # create table
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref("users", passive_deletes=True))
