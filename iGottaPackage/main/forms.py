from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from iGottaPackage.models import User
from iGottaPackage import images


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


# todo: allow image upload here
class BathroomForm(FlaskForm):
    bathroom_name = StringField(_l('Bathroom Name'), validators=[DataRequired()])
    # todo: should location be int or string? Check parsing
    bathroom_about = TextAreaField(_l('Bathroom About'), validators=[DataRequired()])
    bathroom_address = StringField(_l('Bathroom Address'), validators=[DataRequired()])
    bathroom_image = FileField(_l('Bathroom Photo'), validators=[FileRequired(), FileAllowed(images, _('Images Only!'))])
    submit = SubmitField(_l('Submit'))
