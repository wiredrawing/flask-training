import bcrypt
from marshmallow import Schema, fields, pprint, ValidationError, validate
from sqlalchemy.orm import Query

from lib.logger import get_app_logger
from lib.setting import session
from models.User import User
from routes.CreateRoomForm import check_word_length


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


class CreateUpdatingPasswordForm(Schema):

    # どうもSchemaクラスはシングルトンで実行されている
    # ようなので,コンストラクタでvalidatorsを削除する
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for key in list(self.fields):
    #         # バリデーションルールを空っぽに
    #         self.fields[key].validators = []

    user_id = fields.Integer(required=True, error_messages={"required": "ユーザーIDは必須項目です"})

    current_password = fields.String(required=True, error_messages={"required": "現在のパスワードは必須項目です"})

    new_password = fields.String(required=True, error_messages={"required": "新しいパスワードは必須項目です"})

    new_password_confirm = fields.String(required=True, error_messages={"required": "確認用パスワードは必須項目です"})
