from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional, Length
from iGottaPackage.models import User, Post, Bathroom


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddBathroomForm(FlaskForm):
    lat = FloatField('latitude', validators=[DataRequired()])
    lng = FloatField('longitude', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    # picture = FileField('Picture', validators=[FileRequired()])
    picture = FileField('Picture', validators=[Optional()])
    body = TextAreaField('Description', validators=[Length(min=0, max=280)])
    submit = SubmitField('Add it')

    def validate_location(self, lat, lng):
        lat = Bathroom.query.filter_by(lat=lat.data).first()
        lng = Bathroom.query.filter_by(lng=lng.data).first()
        if (lat is not None) and (lng is not None):
            raise ValidationError('This location has already been registered.')

# validate photo properties?