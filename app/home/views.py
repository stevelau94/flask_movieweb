# coding:utf-8

from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm, UserdetialForm, PwdForm
from app.models import User, Userlog, Preview, Tag, Movie
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db, app
from functools import wraps
import uuid
import os
import datetime


# 访问控制
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if not session.has_key("admin") or session["admin"] is None:
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称，使文件具有唯一性名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)  # 将名称分割
    # fileinfo[-1]表示取文件后缀
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@home.route("/", methods=['GET'])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(tag_id=int(star))
    # 上映时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()  # 升序
            )
    # 播放量
    play_num = request.args.get('play_num', 0)
    if int(play_num) != 0:
        if int(play_num) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()  # 升序
            )
    # 评论量
    comment_num = request.args.get('comment_num', 0)
    if int(comment_num) != 0:
        if int(comment_num) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()  # 升序
            )
    # 分页
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)

    p = dict(
        tid=tid,
        star=star,
        time=time,
        play_num=play_num,
        comment_num=comment_num
    )
    return render_template("home/index.html", tags=tags, p=p, page_data=page_data)


@home.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误！', 'error')
            return redirect(url_for("home.login"))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr,
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    session.pop('user', None)
    session.pop('userlog', None)
    return redirect(url_for("home.login"))


# 会员注册
@home.route("/regist/", methods=['GET', 'POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex,
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！", 'ok')
    return render_template("home/regist.html", form=form)


# 会员修改资料
@home.route("/user", methods=['GET', 'POST'])
@user_login_req
def user():
    form = UserdetialForm()
    user = User.query.get(session['user_id'])
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        # 如果上传文件夹不存在，则创建UP_DIR并修改文件权限
        if not os.path.exists(app.config["UserFace_DIR"]):
            os.makedirs(app.config["UserFace_DIR"])
            os.chmod(app.config["UserFace_DIR"], "rw")
        user.face = change_filename(file_face)
        form.face.data.save(app.config["UserFace_DIR"] + user.face)
        # 检测是否存在重复
        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('昵称已经存在', 'error')
            return redirect(url_for('home.user'))
        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash('邮箱已经存在', 'error')
            return redirect(url_for('home.user'))
        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash('手机已经存在', 'error')
            return redirect(url_for('home.user'))
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash("修改成功！", 'ok')
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


@home.route("/pwd/", methods=['GET', 'POST'])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session["user"]).first()
        if not user.check_pwd(data['old_pwd']):
            flash('密码错误！', 'error')
            # 这里一定要return
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data["new_pwd"])  # 生成新密码
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功! 请重新登陆!", "ok")
        # 这里一定要return
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html", form=form)


@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")


@home.route("/loginlog/<int:page>/", methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id=int(session['user_id'])
    ).order_by(  # 数据库查询
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=5)
    return render_template("home/loginlog.html", page_data=page_data)


@home.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")


# 上映预告
@home.route("/animation/")
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html", data=data)


@home.route("/search/")
def search():
    return render_template("home/search.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")
