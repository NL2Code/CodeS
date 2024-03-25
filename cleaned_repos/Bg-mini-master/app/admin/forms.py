from flask.ext.wtf import Form
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..main.forms import CommentForm


class CommonForm(Form):
    types = SelectField("博文分类", coerce=int, validators=[DataRequired()])
    source = SelectField("博文来源", coerce=int, validators=[DataRequired()])


class SubmitArticlesForm(CommonForm):
    title = StringField("标题", validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField("博文内容", validators=[DataRequired()])
    summary = TextAreaField("博文摘要", validators=[DataRequired()])


class ManageArticlesForm(CommonForm):
    pass


class DeleteArticleForm(Form):
    articleId = StringField(validators=[DataRequired()])


class DeleteArticlesForm(Form):
    articleIds = StringField(validators=[DataRequired()])


class DeleteCommentsForm(Form):
    commentIds = StringField(validators=[DataRequired()])


class AdminCommentForm(CommentForm):
    article = StringField(validators=[DataRequired()])


class AddArticleTypeForm(Form):
    name = StringField("分类名称", validators=[DataRequired(), Length(1, 64)])
    introduction = TextAreaField("分类介绍")
    setting_hide = SelectField("属性", coerce=int, validators=[DataRequired()])
    menus = SelectField("所属导航", coerce=int, validators=[DataRequired()])


# You must add coerce=int, or the SelectFile validate function only validate the int data


class EditArticleTypeForm(AddArticleTypeForm):
    articleType_id = StringField(validators=[DataRequired()])


class AddArticleTypeNavForm(Form):
    name = StringField("导航名称", validators=[DataRequired(), Length(1, 64)])


class EditArticleNavTypeForm(AddArticleTypeNavForm):
    nav_id = StringField(validators=[DataRequired()])


class SortArticleNavTypeForm(AddArticleTypeNavForm):
    order = StringField("序号", validators=[DataRequired()])


class CustomBlogInfoForm(Form):
    title = StringField("博客标题", validators=[DataRequired()])
    signature = TextAreaField("个性签名", validators=[DataRequired()])
    navbar = SelectField("导航样式", coerce=int, validators=[DataRequired()])


class AddBlogPluginForm(Form):
    title = StringField("插件名称", validators=[DataRequired()])
    note = TextAreaField("备注")
    content = TextAreaField("内容", validators=[DataRequired()])


class ChangePasswordForm(Form):
    old_password = PasswordField("原来密码", validators=[DataRequired()])
    password = PasswordField(
        "新密码", validators=[DataRequired(), EqualTo("password2", message="两次输入密码不一致！")]
    )
    password2 = PasswordField("确认新密码", validators=[DataRequired()])


class EditUserInfoForm(Form):
    username = StringField("昵称", validators=[DataRequired()])
    email = StringField("电子邮件", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("密码确认", validators=[DataRequired()])
