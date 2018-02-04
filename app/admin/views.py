# coding:utf-8

from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
from functools import wraps
from app import db


# 访问控制
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if not session.has_key("admin") or session["admin"] is None:
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


@admin.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # 进行提交验证
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误！")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]  # 若密码正确则保存会话
        return redirect(request.args.get('next') or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("admin", None)  # 退出系统 会话删掉admin
    return redirect(url_for("admin.login"))


@admin.route("/pwd")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 添加标签
@admin.route("/tag/add", methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("标签名称已经存在！", "error")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(  # 若标签不存在则进行入库
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功！", "ok")
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(  # 分页
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功！", "ok")
    return redirect(url_for('admin.tag_list', page=1))  # 记得给页码


# 编辑标签
@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and tag_count == 1:
            flash("标签名称已经存在！", "error")
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功！", "ok")
        redirect(url_for("admin.tag_edit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


@admin.route("/movie/add")
@admin_login_req
def movie_add():
    return render_template("admin/movie_add.html")


@admin.route("/movie/list")
@admin_login_req
def movie_list():
    return render_template("admin/movie_list.html")


@admin.route("/preview/add")
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")


@admin.route("/preview/list")
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")


@admin.route("/user/list")
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


@admin.route("/user/view")
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


@admin.route("/comment/list")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")


@admin.route("/moviecol/list")
@admin_login_req
def moviecol_list():
    return render_template("admin/moviecol_list.html")


@admin.route("/oplog/list")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")


@admin.route("/adminloginlog/list")
@admin_login_req
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


@admin.route("/userloginlog/list")
@admin_login_req
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


@admin.route("/auth/add")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/auth/list")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")


@admin.route("/role/add")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role/list")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/admin/add")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")


@admin.route("/admin/list")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")
