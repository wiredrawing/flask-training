# from wtforms import Form, StringField, validators, ValidationError, IntegerField

from lib.setting import session
from models.Message import Message
from marshmallow import Schema, fields, pprint, ValidationError


def check_message_id(message_id):
    """
    メッセージIDが存在するかチェックする
    :param message_id:
    :return:
    """
    message = session.query(Message).filter(Message.id == message_id).first()
    if message is None:
        raise ValidationError("Could not find the message id that you specified.")


class CreateNewLikeForm(Schema):
    message_id = fields.Integer(required=True, validate=check_message_id)
    user_id = fields.Integer(required=True)
