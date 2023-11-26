from marshmallow import Schema, fields, pprint, ValidationError
from lib.setting import session
from models.Room import Room
from models.User import User


def check_room_id(room_id):
    room = session.query(Room).filter(
        Room.id == room_id,
    ).first()
    if room is None:
        raise ValidationError("指定されたルームIDは存在しません")
    return True


def check_user_id(user_id):
    """
    ユーザーIDが存在するかチェックする
    :param user_id:
    :return:
    """
    user = session.query(User).filter(
        User.id == user_id,
    ).first()
    if user is None:
        raise ValidationError("指定されたユーザーIDは存在しません")
    return True


class CreateMessageForm(Schema):
    """
    メッセージの作成フォーム
    """
    message = fields.String(required=True)
    room_id = fields.Integer(required=True, validate=check_room_id)
    user_id = fields.Integer(required=True, validate=check_user_id)

# class CreateMessageForm(Form):
#     """
#     メッセージの作成フォーム
#     """
#     message = StringField("メッセージ", [
#         validators.DataRequired(message="メッセージは必須項目です")
#     ], default="")
#
#     room_id = IntegerField("ルームID", [
#         validators.DataRequired(message="ルームIDは必須項目です"),
#         check_room_id
#     ]);
#
#     user_id = IntegerField("ユーザーID", [
#         validators.DataRequired(message="ユーザーIDは必須項目です"),
#         check_user_id
#     ]);
