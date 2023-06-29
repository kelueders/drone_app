from flask import Blueprint, render_template, request, redirect, url_for, flash
from drone_inventory.forms import UserLoginForm
from drone_inventory.models import User, db, check_password_hash

from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')         # creating a Blueprint with name 'auth'

@auth.route('/signup', methods = ['GET', 'POST'])       # methods always goes inside a list no matter how many elements there are
def signup():
    userform = UserLoginForm()

    try:
        if request.method == 'POST' and userform.validate_on_submit():            # once click submit GET will change to POST
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data
            print(email, password)

            user = User(email, username, password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.signin'))
        
    except:
        raise Exception('Invalid Form Data. Please check your form.')
    
    return render_template('signup.html', form = userform)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    userform = UserLoginForm()


    try:
        if request.method == "POST" and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data 
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()    # if the user email matches the email we are checking against
            if logged_user and check_password_hash(logged_user.password, password):      # if we return something from the query above on line 46
                login_user(logged_user)
                flash('You were sucessfully signed in via: Email/Password', 'auth-success')
                return redirect(url_for('site.profile'))       # come back to here and redirect to profile
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
            
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form = userform)

@auth.route('/logout')        # if it doesn't have any methods it will auto default to 'GET'
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

# now have created the Blueprint, so need to IMPORT then REGISTER it into the __init__.py