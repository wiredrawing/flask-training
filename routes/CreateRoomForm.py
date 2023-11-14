from wtforms import Form, StringField, validators, ValidationError, IntegerField


class CreateRoomForm(Form):
    """新規チャットルームの作成フォーム"""
    room_name = StringField('ルーム名', [
        validators.DataRequired(message="ルーム名は必須項目です"),
    ], default="")

    description = StringField("ルーム概要説明", [
        validators.DataRequired(message="ルーム概要説明は必須項目です")
    ], default="")
