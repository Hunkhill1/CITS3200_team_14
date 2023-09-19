from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, logout_user
from config import Config
from app.routes import index, unit
from app.forms import LoginForm
from app.models import User
from app import db
#from staff_editing_blueprint import staff_editing_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(index)
app.register_blueprint(unit, url_prefix='/unit')
#app.register_blueprint(staff_editing_bp)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('staff_editing'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()  # Log the user out
    flash('Logged out successfully!')
    dummy_form = LoginForm()
    return render_template('login.html', title='Sign In', form=dummy_form)  # Redirect to the login page after logout

@app.route('/planner', methods=['GET'])
def planner():
    return render_template('planner.html', title='Unit Planner')

@app.route('/staff_editing')
def staff_editing():
    return render_template('staff_editing.html', title='Staff Editing Page')

if __name__ == '__main__':
    app.run(debug=True)


