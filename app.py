from flask import (
    Flask,
    redirect,
    render_template,
    request,
    flash,
    url_for
)
# from flask_restful import Api, Resource
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField
)
from wtforms.validators import (
    InputRequired,
    Email,
    Length,
    DataRequired,
    EqualTo
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123Password!@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '67eb24a85f65415033258e7f13d2a81bf67542a2ac608768'
db = SQLAlchemy(app)
# api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=16)])
    email = StringField('Email address',
                        validators=[InputRequired(), Length(max=50), Email(message='Invalid email address')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), DataRequired(),
                                                     EqualTo('confirm', message='Passwords must be the same')])
    confirm = PasswordField('Repeat password',
                            validators=[InputRequired(), EqualTo('password', message='Passwords must be the same')])
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return "You've send POST request"
    else:
        return "<h1>You've send GET request</h1>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        return f'<h1>{form.username.data} {form.password.data}</h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        return f'<h1>{form.username.data} {form.email.data} {form.password.data}</h1>'
    return render_template('signup.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    print('Creating Database...')
    db.create_all()
    print('Done')
    app.run()
