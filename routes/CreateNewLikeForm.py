# from wtforms import Form, StringField, validators, ValidationError, IntegerField
from lib.logger import get_app_logger
from lib.setting import session
from models.Message import Message
from marshmallow import Schema, fields, pprint, ValidationError, validate

from models.User import User


def check_message_id(message_id):
    """
    メッセージIDが存在するかチェックする
    :param message_id:
    :return:
    """
    message = session.query(Message).filter(Message.id == message_id).first()
    if message is None:
        raise ValidationError("Could not find the message id that you specified.")


# httpリクエストbodyをアタッチしたclassを返却する
def get_create_new_like_schema(login_user_id: int):
    get_app_logger(__name__).info("スキーマクラスを関数でラップしてそのクラスを返却する")

    # クラス属性に動的な値をバインドしてクラス定義したい.
    class CreateNewLikeForm(Schema):
        message_id = fields.Integer(required=True, validate=check_message_id)
        user_id = fields.Integer(required=True, validate=(
                # postされたuser_idとログイン中のuser_idがマッチするかどうかを検証
                validate.Equal(login_user_id, error="ログイン中のユーザーIDと一致しません")
            )
        )

    return CreateNewLikeForm
