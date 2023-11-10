from wtforms import Form, StringField, validators, ValidationError, IntegerField

from lib.setting import session
from models.Room import Room
from models.User import User


def check_user_id(form, field):
    """ユーザーIDが存在するかチェックする"""
    user = session.query(User).filter(User.id == field.data).first()
    if user is None:
        raise ValidationError("指定されたユーザーIDは存在しません")

    # バリデーションとして問題ない場合
    # 値を返して問題ないのか不明
    return user.id;


def check_room_id(form, field):
    room = session.query(Room).filter(Room.id == field.data).first()
    if room is None:
        raise ValidationError("指定されたルームIDは存在しません")
    return room.id


class CreateParticipantForm(Form):
    user_id = IntegerField("ユーザーID", [
        validators.DataRequired(message="ユーザーIDは必須項目となります"),
        # データベースに存在するuser_idであることを保証する
        check_user_id
    ])

    room_id = IntegerField("ルームID", [
        validators.DataRequired(message="ルームIDは必須項目となります"),
        # データベースに存在するroom_idであることを保証する
        check_user_id
    ])
