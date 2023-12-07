import bcrypt
from marshmallow import Schema, fields, pprint, ValidationError, validate
from sqlalchemy.orm import Query

from lib.setting import session
from models.User import User
from routes.CreateRoomForm import check_word_length


class CheckCurrentPassword(validate.Validator):

    def __init__(self, user_id: int, users: Query, error=None):
        self.user_id = user_id
        self.users = users
        self.error = error

    def __call__(self, value):
        # パスワードをチェックする対象のユーザーを取得
        user = self.users.filter(User.id == self.user_id).first()
        if user is None:
            raise ValidationError(self.error)
        # value => 現在のパスワード
        # blowfishでハッシュ化する
        # saltの生成
        print(user.password)
        is_match = bcrypt.checkpw(value.encode("utf-8"), user.password.encode("utf-8"))
        if is_match is False:
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


class CreateUpdatingPasswordForm(Schema):
    user_id = fields.Integer(required=True, error_messages={"required": "ユーザーIDは必須項目です"})

    current_password = fields.String(required=True, error_messages={"required": "現在のパスワードは必須項目です"})

    new_password = fields.String(required=True,  error_messages={"required": "新しいパスワードは必須項目です"})

    new_password_confirm = fields.String(required=True, error_messages={"required": "確認用パスワードは必須項目です"})
