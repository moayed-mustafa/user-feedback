# Notes to self:
    # make the routes restful
    # make one route for showing the user's page and adding a new feedback


from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import SignUpForm, LoginForm, FeedbackForm
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',"postgres:///feedback_db" )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", '123asd')
print("==============================================================================================================================")
print(app.config["SECRET_KEY"])
print("==============================================================================================================================")


connect_db(app)
db.create_all()

@app.route('/')
def home_route():
    if 'username' in session:
        username = session['username']
        return redirect(f'/user/{username}')
    return redirect('/register')


    # =======================================================================================================
# register a user
@app.route('/register',methods=["GET", "POST"])
def register_route():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.firstname.data
        last_name = form.lastname.data
        email = form.email.data
        pw = form.password.data
        existing_user = User.query.get(username)
        # if the name is not preesnt on the database/username not taken
        if existing_user is None:
            # register the user
            new_user = User.register(username, pw, first_name, last_name, email)
            db.session.add(new_user)
            db.session.commit()

            session['username'] = new_user.username
            return redirect(f'/user/{username}')
            # username is present on the database/already taken
        else:
            # session.pop('_flashes', None)
            form.username.errors=['A user with this name already exists! please choose another username']
            # flash('A user with this name already exists! please choose another username')
            return render_template('register.html', form=form)

    else:

        return render_template('register.html', form=form)
     # =======================================================================================================
# login a user
@app.route('/login', methods=["GET", "POST"])
def login_route():
    if 'username' in session:
        flash(' You are already logged in')
        username = session['username']
        return redirect(f'/user/{username}')

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        pw = form.password.data
        existing_user = User.authenticate(username, pw)
        if existing_user:
            session['username'] = existing_user.username
            flash(f"Welcome back {existing_user.username}", 'success')
            return redirect(f'/user/{username}')
        else:
            # emptying the flash object
            session.pop('_flashes', None)
            # flash('either password or username is not correct!')
            form.username.errors=['invalid username/password']
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
    # =======================================================================================================
# show a usre's feedbackpage
@app.route('/user/<string:username>', methods=["GET", "POST"])
def timeline(username):
    # only allow logged in users to get here
    if 'username' not in session:
        flash('You need to log in first', category='primary')
        return redirect('/login')
    else:

        user = User.query.get(username)
        feedbacks = Feedback.query.filter(Feedback.username == username).all()
        return render_template('userpage.html', user=user, feedbacks=feedbacks)

    # =======================================================================================================
# allow the user to add a feedback
@app.route('/user/<string:username>/feedback', methods=["GET", "POST"])
def feedback(username):
    if 'username' not in session:
        flash('You have to log in first', category='primary')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        feedback = form.feedback.data
        username = session['username']
        new_feedback = Feedback(username=username, content=feedback, title=title)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/user/{username}')
    else:
        # session.pop("errors", None)
        return render_template('feedbackform.html', form=form)



    # =======================================================================================================
# logout a user
@app.route('/logout',methods=["GET", "POST"])
def logout_route():
    if 'username' not in session:
        flash('log in first', 'danger')
        return redirect('/login')

    username = session['username']
    flash(f"goodbye {username}", 'success')
    session.pop('username', None)
    return redirect('/')
    # =======================================================================================================
# delete a user
@app.route('/user/<username>/delete',methods=["GET", "POST"])
def delete_route(username):
    if 'username' not in session:
        flash('You need to log in first', category='primary')
    else:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        flash('user has been deleted', category='success')
        session.pop('username', None)
        return redirect('/login')

    # =======================================================================================================
# edit a feedback
@app.route('/edit/<username>/feedback/<int:id>',methods=["GET", "POST"])
def edit_feedback(username, id):
    if 'username' not in session or session['username'] != username:
        flash('You need to log in first/not the right credintials', category='primary')
        return redirect('/login')
    else:

        feedback = Feedback.query.filter_by(id=id).first()

        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            title = form.title.data
            fb = form.content.data
            feedback.title = title
            feedback.content = fb
            db.session.commit()
            flash('feedback edited!', category='success')
            return redirect(f'/user/{username}')
        else:
            return render_template('feedbackform.html', form=form)
    # =======================================================================================================
# delete a feedback
@app.route('/user/<username>/delete-feedback/<int:id>',methods=["GET", "POST"])
def delete_feedback(username, id):
    if 'username' not in session or session['username'] != username:
        flash('You need to log in first/not the right credintials', category='primary')
        return redirect('/login')
    fb = Feedback.query.filter_by(id=id).first()
    if fb.username == username:
        db.session.delete(fb)
        db.session.commit()
        flash('Feedback Deleted!', category='success')
        return redirect(f'/user/{username}')

