from marshmallow import Schema, fields


class CreateUpdateUserInfoForm(Schema):
    """Form for creating and updating user info."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key in list(self.fields):
            # バリデーションルールを空っぽに
            self.fields[key].validators = []

    # usernameカラム
    username = fields.String(
        required=True,
        error_messages={"required": "ユーザー名は必須項目です"}
    )

    id = fields.Integer(
        required=True,
        error_messages={"required": "ユーザーIDは必須項目です"}
    )

    email = fields.Email(
        required=True,
        error_messages={"required": "メールアドレスは必須項目です"}
    )
