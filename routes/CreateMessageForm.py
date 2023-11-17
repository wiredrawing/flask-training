from wtforms import Form, StringField, validators, ValidationError, IntegerField

from lib.setting import session
from models.Room import Room
from models.User import User


def check_room_id(form, field):
    room = session.query(Room).filter(
        Room.id == field.data,
    ).first()
    if room is None:
        raise ValidationError("指定されたルームIDは存在しません")
    else:
        return None


def check_user_id(form, field):
    """
    フォームから投稿されたユーザーIDが存在するかチェックする
    :param form:
    :param field:
    :return:
    """
    user = session.query(User).filter(
        User.id == field.data,
    ).first()
    if user is None:
        raise ValidationError("指定されたユーザーIDは存在しません")
    else:
        return None


class CreateMessageForm(Form):
    """
    メッセージの作成フォーム
    """
    message = StringField("メッセージ", [
        validators.DataRequired(message="メッセージは必須項目です")
    ], default="")

    room_id = IntegerField("ルームID", [
        validators.DataRequired(message="ルームIDは必須項目です"),
        check_room_id
    ]);

    user_id = IntegerField("ユーザーID", [
        validators.DataRequired(message="ユーザーIDは必須項目です"),
        check_user_id
    ]);
