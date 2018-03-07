# coding: utf-8
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

from app.models import User


class RegistForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称！")
        ],
        description="昵称",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control input-lg",
            'placeholder': "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！"),
            Email('邮箱格式不正确!')
        ],
        description="邮箱",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control input-lg",
            'placeholder': "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机！"),
            # 使用正则表达式验证手机格式
            Regexp("1[3458]\\d{9}", message="手机号码格式不正确！")
        ],
        description="手机",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control input-lg",
            'placeholder': "请输入邮箱！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！这是验证器！")
        ],
        description="密码",
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码！",
            'required': "required"
        }
    )
    repwd = PasswordField(
        label="重新输入密码",
        validators=[
            DataRequired("请重新输入密码！"),
            EqualTo('pwd', message="两次密码不一致！")  # 验证两次输入的密码是否一致
        ],
        description="重新输入密码",
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请重新输入密码！",
            'required': "required"
        }
    )

    submit = SubmitField(  # 按钮
        "注册",
        render_kw={
            'class': "btn btn-lg btn-success btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("昵称已经存在！")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在！")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机已经存在！")


class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control",
            'placeholder': "请输入账号！",
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
            'class': "btn btn-lg btn-primary btn-block",
        }
    )


class UserdetialForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称！")
        ],
        description="昵称",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control",
            'placeholder': "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！"),
            Email('邮箱格式不正确!')
        ],
        description="邮箱",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control",
            'placeholder': "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机！"),
            # 使用正则表达式验证手机格式
            Regexp("1[3458]\\d{9}", message="手机号码格式不正确！")
        ],
        description="手机",
        render_kw={  # 原模板中相关模块的其他定义，以便wtforms生成H5
            'class': "form-control",
            'placeholder': "请输入邮箱！",
        }
    )

    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像！")
        ],
        description="头像",
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
    submit = SubmitField(  # 按钮
        '保存修改',
        render_kw={
            'class': "btn btn-success",
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
        "修改密码",
        render_kw={
            'class': "btn btn-success",
        }
    )


class CommentForm(FlaskForm):
    content = TextAreaField(
        label='内容',
        validators=[
            DataRequired("请输入评论！")
        ],
        description="评论内容",
        render_kw={
            # "class": "form-control",
            "id": "input_content"
        }
    )
    submit = SubmitField(  # 按钮
        "提交评论",
        render_kw={
            'class': "btn btn-success",
            'id': "btn-sub"
        }
    )
