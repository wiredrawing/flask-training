from wtforms import Form, StringField, validators, ValidationError, IntegerField

from lib.setting import session
from models.User import User
from models.Room import Room
from validators.CheckMessageId import check_message_id
from validators.CheckUserId import check_user_id


class CreateNewLikeForm(Form):
    """
    いいねの作成フォーム
    """
    user_id = IntegerField("ユーザーID", [
        validators.DataRequired(message="ユーザーIDは必須項目です"),
        check_user_id(session=session, message="指定されたユーザーIDは存在しません")
    ]);

    message_id = IntegerField("メッセージID", [
        validators.DataRequired(message="メッセージIDは必須項目です"),
        check_message_id(session=session, message="指定されたメッセージIDは存在しません")
    ]);
