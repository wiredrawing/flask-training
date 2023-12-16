from marshmallow import Schema, fields, validate

from lib.setting import session
from models.User import User
from routes.CreateUpdatingPasswordForm import CheckUserExisting


class CheckEmailExisting(validate.Validator):
    """メールアドレスが既に存在しているかチェックするバリデーター

    DB上に登録されるメールアドレスは常に一意である必要がある"""
    def __init__(self, user_id: int, users, error="既に存在しているメールアドレスです"):
        print("session.query(User)'s type is ", type(users))
        self.error = error
        self.users = users
        self.user_id = user_id

    def __call__(self, value):
        """自分自身以外で同一のメールアドレスがあった場合不正とする"""
        user = self.users.filter(User.email == value).filter(User.id != self.user_id).first()
        print(user)
        if user is not None:
            raise validate.ValidationError(self.error)
        return value


def get_create_update_user_info_schema(login_user_id: int, post_data: dict):
    class CreateUpdateUserInfoForm(Schema):
        """Form for creating and updating user info."""
        # usernameカラム
        username = fields.String(
            required=True,
            validate=[
                validate.Length(min=4, max=64, error="ユーザー名は1文字以上20文字以下で入力してください")
            ],
            error_messages={"required": "ユーザー名は必須項目です"}
        )

        id = fields.Integer(
            required=True,
            error_messages={"required": "ユーザーIDは必須項目です"},
            validate=[
                CheckUserExisting(session.query(User), error="ユーザーIDが一致しません"),
                validate.Equal(login_user_id, error="ユーザーIDが一致しません")
            ]
        )

        email = fields.Email(
            required=True,
            error_messages={"required": "メールアドレスは必須項目です"},
            validate=[
                validate.Email(error="メールアドレスの形式が不正です"),
                CheckEmailExisting(login_user_id, session.query(User))
            ],
        )

    return CreateUpdateUserInfoForm
