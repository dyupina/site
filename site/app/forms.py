from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    SNs = SelectMultipleField('SNs', validators=[InputRequired()], choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    user_type = BooleanField('Administrator')
    submit = SubmitField('Add New User')

class ChoseData(FlaskForm):
    SNs = SelectField('SNs', coerce=int, validators=[InputRequired()], choices=[])
    start = DateField('DatePickerStart', format='%Y-%m-%d')
    end = DateField('DatePickerEnd', format='%Y-%m-%d')
    submit = SubmitField('Посмотреть таблицу')

class MakeChartForm(FlaskForm):
    submit = SubmitField('Построить график')

