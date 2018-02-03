# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin


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

    submit = SubmitField(
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

