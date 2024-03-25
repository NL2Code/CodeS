from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class CommentForm(Form):
    name = StringField("昵称", validators=[DataRequired()])
    email = StringField("邮箱", validators=[DataRequired(), Length(1, 64), Email()])
    content = TextAreaField("内容", validators=[DataRequired(), Length(1, 1024)])
    follow = StringField(validators=[DataRequired()])
