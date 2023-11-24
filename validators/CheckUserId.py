from sqlalchemy.orm import Session
from wtforms import ValidationError

from models.User import User


def check_user_id(session: Session, message="指定されたユーザーIDは存在しません"):
    def inner(form, field):
        user = session.query(User).filter(
            User.id == field.data,
        ).first()
        if user is None:
            raise ValidationError(message)
        else:
            return None

    return inner
