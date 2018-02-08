# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag

tags = Tag.query.all()  # 数据库中查询tags


class LoginForm(FlaskForm):
    """管理员登陆表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！这是验证器！")
        ],
        description="账号",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control",
            'placeholder': "请输入账号！",
            'required': "required"  # 如果表单没有内容输入，会出现气泡框警告；此功能和上面的validators有些类似，所以上面警告不会显示出来
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！这是验证器！")
        ],
        description="密码",
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码！",
            'required': "required"
        }
    )

    submit = SubmitField(  # 按钮
        "登陆",
        render_kw={
            'class': "btn btn-primary btn-block btn-flat",
        }
    )

    # 自定义验证器
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()  # 查询数据库中是否存在此用户
        if admin == 0:
            raise ValidationError("账号不存在！")  # 如果无此用户，则抛出ValidationError


class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签！")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )

    submit = SubmitField(  # 按钮
        "编辑",
        render_kw={
            'class': "btn btn-primary",
        }
    )


class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入影片名称！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "row": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )

    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )

    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control",
        }
    )

    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入影片地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入影片片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间",
            "id": "input_release_time"  # HTML文件中有相关控件实现时间选择
        }
    )
    submit = SubmitField(  # 按钮
        "编辑",
        render_kw={
            'class': "btn btn-primary",
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label="预告影片",
        validators=[
            DataRequired("请输入预告影片！")
        ],
        description="预告影片",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告影片！"
        }
    )
    logo = FileField(
        label="预告影片封面",
        validators=[
            DataRequired("请上传预告影片封面！")
        ],
        description="预告影片封面",
    )
    submit = SubmitField(  # 按钮
        "编辑",
        render_kw={
            'class': "btn btn-primary",
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！"
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(  # 按钮
        "编辑",
        render_kw={
            'class': "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误")
