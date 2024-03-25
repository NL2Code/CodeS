from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, abort, make_response, g, current_app
from flask_login import current_user, login_required

from .. import db
from . import user
from .forms import ProfileForm, PostForm, CommentForm, ReplyForm, SearchForm, EditpostForm
from ..models import User, Post, Comment, Like, Permission, Admin
from ..decorators import permission_required


@user.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.add(current_user)
        db.session.commit()
    g.search_form = SearchForm()

@user.route('/')
@user.route('/index')
def index():
    notice = Admin.query.order_by(Admin.timestamp.desc()).first()
    if notice:
        notice=notice.notice
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    # posts = pagination.items
    posts = [post for post in pagination.items if post.draft==False]
    return render_template('user/index.html',
                           title = 'Homepage',
                           posts=posts,
                           notice=notice,
                           pagination=pagination)

@user.route('/user/<nickname>')
# @login_required
def users(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('Not find：' + nickname)
        return redirect(url_for('user.index'))
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    posts = [post for post in posts if post.draft == False]
    return render_template('user/user.html',
                           user=user,
                           posts=posts,
                           title='Personal Profile')

@user.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Change successful!')
        return redirect(url_for('user.users',nickname=current_user.nickname))
    else:
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me
    return render_template('user/editprofile.html',
                           form=form,
                           title='Edit Profile')

@user.route('/write', methods=['GET','POST'])
def write():
    form = PostForm()
    if current_user.operation(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        if 'save_draft' in request.form and form.validate():
            post = Post(body=form.body.data,
                        title=form.title.data,
                        draft= True,
                        author = current_user._get_current_object())
            db.session.add(post)
            flash('Save successful!')
        elif 'submit' in request.form and form.validate():
            post = Post(body=form.body.data,
                        title=form.title.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            flash('Publish successful!')
        return redirect(url_for('user.write'))
    return render_template('user/write.html',
                           form=form,
                           post=form.body.data,
                           title='Write Posts')

@user.route('/draft/')
@login_required
def draft():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    drafts = [post for post in posts if post.draft==True]

    return render_template('user/draft.html',
                           title='Draft',
                           pagination=pagination,
                           drafts=drafts)

@user.route('/delete-draft/<int:id>')
@login_required
def delete_draft(id):
    draft = Post.query.get_or_404(id)
    draft.disabled = True
    db.session.add(draft)
    flash('Delete successful!')
    return redirect(url_for('user.draft'))


@user.route('/post/<int:id>', methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    post.view_num += 1
    db.session.add(post)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post, unread=True,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published successfully.')
        return redirect(url_for('user.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('user/post.html', posts=[post],
                           title=post.title, id=post.id,
                           post=post, form=form,
                           comments=comments,
                           pagination=pagination)

@user.route('/like/<int:id>')
@login_required
def like(id):
    post = Post.query.get_or_404(id)

    if post.like_num.filter_by(liker_id=current_user.id).first() is not None:
        flash('You\'ve liked it.')
        return redirect(url_for('user.post', id=post.id))
    like = Like(post=post, unread=True,
                user=current_user._get_current_object())
    db.session.add(like)
    flash('Like successful!')
    return redirect(url_for('user.post', id=post.id))

@user.route('/unlike/<int:id>')
@login_required
def unlike(id):
    post = Post.query.get_or_404(id)
    if post.like_num.filter_by(liker_id=current_user.id).first() is None:
        flash('You have not liked it yet.')
        return redirect(url_for('user.post', id=post.id))
    # like = Like(post=post,
    #             user=current_user._get_current_object())
    else:
        f = post.like_num.filter_by(liker_id=current_user.id).first()
        db.session.delete(f)
        flash('Likes have been cancelled.')
        return redirect(url_for('user.post', id=post.id))

@user.route('/reply/<int:id>', methods=['GET','POST'])
@login_required
def reply(id):
    comment = Comment.query.get_or_404(id)
    post = Post.query.get_or_404(comment.post_id)
    page = request.args.get('page', 1, type=int)
    form = ReplyForm()
    if form.validate_on_submit():
        reply_comment = Comment(body=form.body.data,
                                unread=True,
                                post=post,comment_type='reply',
                                reply_to=comment.author.nickname,
                                author=current_user._get_current_object())
        db.session.add(reply_comment)
        flash('Your reply has been published.')
        return redirect(url_for('user.post', id=comment.post_id, page=page))
    return render_template('user/reply.html',
                           form=form,
                           comment=comment,
                           title='Reply')

@user.route('/recover/<int:id>')
@login_required
def recover(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post_id
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('user.post',id=post_id))

@user.route('/delate/<int:id>')
@login_required
def delate(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post_id
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('user.post',id=post_id))

@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.operation(Permission.ADMINISTER):
        abort(403)
    form = EditpostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        if post.draft == True:
            if 'save_draft' in request.form and form.validate():
                db.session.add(post)
                flash('Save successfully!')
            elif 'submit' in request.form and form.validate():
                post.draft = False
                db.session.add(post)
                flash('Publish successfully!')
            return redirect(url_for('user.edit', id=post.id))
        else:
            db.session.add(post)
            flash('Update successfully!')
            return redirect(url_for('user.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('user/editpost.html',
                           form=form,
                           post=post,
                           title='Edit Posts')

@user.route('/follow/<nickname>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('user.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('user.users', nickname=nickname))
    current_user.follow(user)
    flash('You have followed %s。' % nickname)
    return redirect(url_for('user.users', nickname=nickname))

@user.route('/unfollow/<nickname>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('user.index'))
    if not current_user.is_following(user):
        flash('You have unfollowed this user.')
        return redirect(url_for('user.users', nickname=nickname))
    current_user.unfollow(user)
    flash('You have unfollowed %s 。' % nickname)
    return redirect(url_for('user.users', nickname=nickname))


@user.route('/follows/<nickname>')
@login_required
def follows(nickname):

    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('user.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    pagination2 = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))

    if show_followed:
        follows = [{'user': i.follower, 'timestamp': i.timestamp}
                   for i in pagination.items]
    else:
        follows = [{'user': i.followed, 'timestamp': i.timestamp}
                   for i in pagination2.items]

    return render_template('user/follow.html', user=user,
                           title='Follow',
                           show_followed=show_followed,
                           pagination=pagination,
                           Permission=Permission,
                           follows=follows)

@user.route('/followers/<nickname>')
def show_follower(nickname):
    resp = make_response(redirect(url_for('user.follows',nickname=nickname)))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp
@user.route('/followed/<nickname>')
def show_followed(nickname):
    resp = make_response(redirect(url_for('user.follows',nickname=nickname)))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@user.route('/search', methods=['GET','POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('user.index'))
    return redirect(url_for('user.search_results', query=g.search_form.search.data))

@user.route('/search_results/<query>')
def search_results(query):
    results = Post.query.whooshee_search(query).all()
    return render_template('user/search_results.html',
                           query=query,
                           title='Searching results',
                           posts=results)
