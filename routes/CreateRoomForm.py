from wtforms import Form, StringField, validators, ValidationError, IntegerField

from marshmallow import Schema, fields, pprint, ValidationError


class CreateRoomForm(Form):
    """新規チャットルームの作成フォーム"""
    room_name = StringField('ルーム名', [
        validators.DataRequired(message="ルーム名は必須項目です"),
    ], default="")

    description = StringField("ルーム概要説明", [
        validators.DataRequired(message="ルーム概要説明は必須項目です")
    ], default="")


def check_room_name_length(room_name: str):
    if not len(room_name) > 0:
        raise ValidationError("ルーム名は必須項目です")
    return True


def check_room_name_ng_word(room_name: str):
    if room_name == "NG":
        raise ValidationError("NGワードが含まれています")
    return True


def check_word_length(error_message: str):
    def inner(word: str):
        if not len(word) > 0:
            raise ValidationError(error_message)
        return True

    return inner


class CreateNewRoomForm(Schema):
    room_name = fields.String(
        required=True,
        validate=(check_word_length("ルーム名は必須項目となります。"), check_room_name_ng_word,),
        error_messages={"required": "ルーム名は必須項目です", "validate": "NGワードが含まれています"},
    )
    description = fields.String(
        required=True,
        validate=(check_word_length("ルーム概要説明は必須項目となります。"),),
        error_messages={"required": "ルーム概要説明は必須項目です", "validate": "NGワードが含まれています"})
