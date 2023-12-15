import re

import bcrypt
from marshmallow import Schema, fields, pprint, ValidationError, validate
from sqlalchemy.orm import Query

from lib.logger import get_app_logger
from lib.setting import session
from models.User import User


class CheckCurrentPassword(validate.Validator):

    def __init__(self, user_id: int, users: Query, error=None):
        print(">>>>>>>>>>>>>>>>>>>>>>Call CheckCurrentPassword!!!!!!!!!!!")
        self.user_id = user_id
        self.users = users
        self.error = error

    def __call__(self, value):
        get_app_logger(__name__).debug("新規で入力されたパスワード {}".format(value))
        # パスワードをチェックする対象のユーザーを取得
        user = self.users.filter(User.id == self.user_id).first()
        if user is None:
            raise ValidationError(self.error)
        # value => 現在のパスワード
        # blowfishでハッシュ化する
        # saltの生成
        print(value)
        print(user.email)
        print(user.password)

        new_password = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt())
        get_app_logger(__name__).debug("入力されたパスワードのハッシュ値 {}".format(new_password))
        is_match = bcrypt.checkpw(value.encode("utf-8"), user.password.encode("utf-8"))
        get_app_logger(__name__).debug("入力されたパスワード {}".format(value.encode("utf-8")))
        get_app_logger(__name__).debug("現在のパスワード {}".format(user.password.encode("utf-8")))
        get_app_logger(__name__).debug("パスワードの一致 {}".format(is_match))
        if not is_match:
            raise ValidationError(self.error)
        return value;


class CheckUserExisting(validate.Validator):

    def __init__(self, users: Query, error=None):
        self.users = users
        self.error = error

    def __call__(self, value):
        # 指定した<user_id>のレコードが存在するかどうかを検証
        user = self.users.filter(User.id == value).first()
        if user is None:
            raise ValidationError(self.error)
        return value


# パスワードが規程の文字制限を満足しているかどうか
class CheckPasswordRegex(validate.Validator):

    def __init__(self, error="パスワードは半角英数字と記号(_-.@=)をそれぞれ1文字以上含む10文字以上72文字以下で入力してください"):
        self.error = error
        pass

    def __call__(self, value):
        password_pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[_\-\.@\=])[0-9a-zA-Z-\-@\.]{10,72}$'
        compiled: re.Pattern = re.compile(password_pattern)
        result = compiled.match(value)
        if result is None:
            raise ValidationError(self.error)
        return value


def get_create_updating_password_schema(post_data: dict, login_user_id: int):
    """バリデートしたい値が動的に変更できないため、関数でラップして動的に値をバインドする"""

    class CreateUpdatingPasswordForm(Schema):
        user_id = fields.Integer(
            required=True,
            validate=[
                validate.Equal(login_user_id, error="ログイン中のユーザーIDと一致しません"),
            ],
            error_messages={"required": "ユーザーIDは必須項目です"}
        )

        current_password = fields.String(
            required=True,
            validate=[
                CheckCurrentPassword(int(post_data["user_id"]), session.query(User), error="現在のパスワードが一致しません")
            ],
            error_messages={"required": "現在のパスワードは必須項目です"}
        )

        new_password = fields.String(
            required=True,
            validate=[
                CheckPasswordRegex(),
                # blowfishの文字制限は72文字まで
                validate.Length(min=8, max=72, error="新しいパスワードは8文字以上で入力してください"),
                validate.Equal(post_data["new_password_confirm"], error="「入力用」新しいパスワードと新しいパスワード(確認用)が一致しません")
            ],
            error_messages={"required": "新しいパスワードは必須項目です"}
        )

        new_password_confirm = fields.String(
            required=True,
            validate=[
                CheckPasswordRegex(),
                # blowfishの文字制限は72文字まで
                validate.Length(min=8, max=72, error="新しいパスワードは8文字以上で入力してください"),
                validate.Equal(post_data["new_password"], error="「確認用」確認用パスワードが新しいパスワードと一致しません")
            ],
            error_messages={"required": "確認用パスワードは必須項目です"}
        )

    return CreateUpdatingPasswordForm
