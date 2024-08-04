from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email.')

class HealthMetricForm(FlaskForm):
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    steps = IntegerField('Steps', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AlertForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Alert')

class LocationForm(FlaskForm):
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Update Location')

class MedicationForm(FlaskForm):
    name = StringField('Medication Name', validators=[DataRequired()])
    dose = StringField('Dose', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    submit = SubmitField('Add Medication')

class ActivityForm(FlaskForm):
    description = TextAreaField('Activity Description', validators=[DataRequired()])
    submit = SubmitField('Log Activity')

class MessageForm(FlaskForm):
    recipient = StringField('Recipient', validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
