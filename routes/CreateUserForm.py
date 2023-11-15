import re

from email_validator import validate_email, EmailNotValidError
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError, IntegerField

from lib.setting import session
from models.User import User


def original_password(message):
    def rule(form, field):
        """パスワードは<記号>,<半角英字の大文字と小文字>,<数字>を含む必要がある"""
        pattern = re.compile(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[_\-\.@\=])[0-9a-zA-Z-\-@\.]{10,72}$')
        if pattern.match(field.data) is None:
            if message:
                raise ValidationError(message)
            else:
                raise ValidationError("パスワードは<記号>,<半角英字の大文字と小文字>,<数字>を含んだものを入力して下さい")

    return rule;


def check_email(form, field):
    try:
        validated_email = validate_email(field.data)
        email = validated_email.normalized
        return None;
    except EmailNotValidError as e:
        raise ValidationError("メールアドレスのフォーマットが不正です")


def duplicate_email(form, field):
    user = session.query(User).filter(
        User.email == field.data,
    ).first()
    if user is not None:
        raise ValidationError("指定されたメールアドレスは使用できません")
    return None


class CreateUserForm(Form):
    """新規ユーザー登録用のフォーム"""
    username = StringField('Username', [
        validators.Length(min=4, max=25, message="ユーザー名は4文字以上25文字以下で入力して下さい"),
    ], default="")
    email = StringField('Email Address', [
        validators.Length(min=6, max=35, message="メールアドレスは6文字以上35文字以下で入力して下さい"),
        check_email,
        duplicate_email,
        # defaultキーワード引数で初期値を設定できる
    ], default="")
    password = PasswordField('New Password', [
        # 独自ルールの追加は,特定のフォーマットで関数を定義する
        original_password(message="指定のフォーマットで入力して下さい"),
        validators.DataRequired(message="パスワードは必須項目となります"),
        validators.EqualTo("confirm", message="You need to input the same password in both fields")
    ]);
    confirm = PasswordField('Repeat Password', [
        # 独自ルールの追加は,特定のフォーマットで関数を定義する
        original_password(message="指定のフォーマットで入力して下さい"),
        validators.DataRequired(message="確認要パスワードは必須項目となります"),
    ])
    gender = IntegerField("性別", [
        validators.DataRequired(message="性別は必須項目となります")
    ], default="0")
