# логика работы программы
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommForm
from flaskblog.models import User, Post, Sportsmen, Event, Comment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

#from flaskblog.forms import EditProfileForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/home")
@login_required
def home():
    posts = Post.query.all()
    #posts = current_user.followed_posts()
    # uss = Us.query.all()
    # channels = Channel.query.all()
    return render_template('home.html', posts=posts)


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')
@app.route("/blog-single")
def blog_single():
    return render_template('blog-single.html')
@app.route("/schedule")
def schedule():
    return render_template('schedule.html')



@app.route("/sportsmen")
def sportsmen():
    sportsmens = Sportsmen.query.all()
    #sposts = current_user.followed_posts()
    return render_template('sportsmen.html', sportsmens=sportsmens, title='Sportsmen')


@app.route("/events")
def event():
    events = Event.query.all()
    return render_template('calendar.html', events=events)



@app.route("/contacts")
def contacts():
    return render_template('contacts.html', title='Contacts')


@app.route("/admin/index")
@login_required
def admin():
    return render_template('admin/index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Аккаунт создан!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Неудачная попытка входа. Проверьте email и пароль', 'danger')
    return render_template('login.html', title='Login', form=form)





@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Аккаунт был обновлен', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Новый пост создан!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>", methods=['POST','GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post.id).all()
    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        comments = Comment(name=current_user.username, email=current_user.email, message=message, post_id = post.id)
        db.session.add(comments)
        post.comments += 1

        flash('Коммент добавлен!', 'success')
        db.session.commit()
        return redirect(request.url)

    return render_template('post.html', title=post.title, post=post, comments=comments)



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Вы обновили свой пост', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Пост удален', 'success')
    return redirect(url_for('home'))



@app.route("/comm/new", methods=['GET', 'POST'])
@login_required
def new_comm():
    form = CommForm()
    if form.validate_on_submit():
        comm = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(comm)
        db.session.commit()
        flash('Новый коммент создан!', 'success')
        return redirect(url_for('home'))
    return render_template('create_comm.html', title='New Comm', form=form, legend='New Comm')



# @app.route("/user/<string:username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)

@app.route('/user/<string:username>', methods=['POST','GET'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts
    sportsmens = Sportsmen.query.all()
    events = Event.query.all()
    return render_template('user.html', posts=posts, user=user, sportsmens=sportsmens, events = events)


@app.route('/sportsmen/<string:name>', methods=['POST','GET'])
@login_required
def sportsmen_profile(name):
    sportsmen = Sportsmen.query.filter_by(name=name).first_or_404()

    return render_template('sport_user.html', sportsmen=sportsmen)








# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('User {} not found.'.format(username))
#         return redirect(url_for('index'))
#     if user == current_user:
#         flash('You cannot follow yourself!')
#         return redirect(url_for('user', username=username))
#     current_user.follow(user)
#     db.session.commit()
#     flash('You are following {}!'.format(username))
#     return redirect(url_for('user', username=username))
#
#
# @app.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('User {} not found.'.format(username))
#         return redirect(url_for('index'))
#     if user == current_user:
#         flash('You cannot unfollow yourself!')
#         return redirect(url_for('user', username=username))
#     current_user.unfollow(user)
#     db.session.commit()
#     flash('You are not following {}.'.format(username))
#     return redirect(url_for('user', username=username))

#

@app.route('/follow/<name>')
@login_required
def follow(name):
    sportsmen = Sportsmen.query.filter_by(name=name).first()
    if sportsmen is None:
        flash('sportsmen {} not found.'.format(name))
        return redirect(url_for('index'))

    current_user.follow(sportsmen)
    db.session.commit()
    flash('You are following {}!'.format(name))
    return redirect(url_for('sportsmen', name=name))


@app.route('/unfollow/<name>')
@login_required
def unfollow(name):
    sportsmen = Sportsmen.query.filter_by(name=name).first()
    if sportsmen is None:
        flash('Sportsmen {} not found.'.format(name))
        return redirect(url_for('index'))


    current_user.unfollow(sportsmen)
    db.session.commit()
    flash('You are not following {}.'.format(name))
    return redirect(url_for('sportsmen', name=name))

