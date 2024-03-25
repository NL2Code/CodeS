from flask import flash, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from ..models import User
from . import auth
from .forms import LoginForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("登陆成功！欢迎回来，%s!" % user.username, "success")
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            flash("登陆失败！用户名或密码错误，请重新登陆。", "danger")
    if form.errors:
        flash("登陆失败，请尝试重新登陆.", "danger")

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("您已退出登陆。", "success")
    return redirect(url_for("main.index"))
