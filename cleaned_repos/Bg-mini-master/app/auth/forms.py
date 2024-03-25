from flask_wtf import Form
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):
    email = StringField("电子邮件", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("密码", validators=[DataRequired()])
