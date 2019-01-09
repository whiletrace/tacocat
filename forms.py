from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (
                                DataRequired, Regexp, ValidationError, Email,
                                EqualTo, Length
                                )