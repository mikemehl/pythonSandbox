from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
   name = StringField('Name', validators=[DataRequired()]);
   msg  = TextAreaField('Message', validators=[DataRequired()]);
   cat = RadioField('Favorite Cat', choices=[('T','Tootsie'),('S','Squeak'), ('N', 'Neither')], validators=[DataRequired()]);
   submit = SubmitField('Sign The Guestbook');
