from marshmallow import Schema, fields, pprint, ValidationError

from lib.logger import get_app_logger
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


def check_ng_message(message):
    if message == "NG":
        raise ValidationError("NGワードが含まれています")
    return True


def check_message_length(message: str):
    if not len(message) > 0:
        raise ValidationError("メッセージの入力は必須項目です。")
    return True


class CreateMessageForm(Schema):

    # 都度バリデーターを空っぽにする
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1957278415696
        get_app_logger(__name__).info("__name__の値 {} CreateMessageFormのインスタンスid => {}".format(__name__, id(self)))
        for key in list(self.fields):
            for validator_rule in self.fields[key].validators:
                get_app_logger(__name__).info("設定中のバリデータールール名{}に対して {}".format(key, str(validator_rule)))
                get_app_logger(__name__).info("バリデータルールのid => {}".format(id(validator_rule)))
            # self.fields内のバリデーションルールをすべて破棄する
            self.fields[key].validators = []

    """
    メッセージの作成フォーム
    """
    message = fields.String(required=True, validate=(check_ng_message, check_message_length), error_messages={"required": "メッセージは必須項目です"})
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
