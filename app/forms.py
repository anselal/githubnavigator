from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_term = StringField('openid', validators=[DataRequired()])
