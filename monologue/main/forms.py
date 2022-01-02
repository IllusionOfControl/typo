from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    body = TextAreaField('Body', validators=[])