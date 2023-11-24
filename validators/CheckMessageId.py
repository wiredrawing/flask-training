from sqlalchemy.orm import Session
from wtforms import ValidationError

from models.Message import Message


# ルームIDが存在するかチェック関数を返却する
def check_message_id(session: Session, message="指定されたメッセージIDは存在しません"):
    def inner(form, field):
        message = session.query(Message).filter(
            Message.id == field.data,
        ).first()
        if message is None:
            raise ValidationError(message)
        else:
            return None

    return inner
