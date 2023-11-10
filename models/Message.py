
# sys.path.append('C:\\Users\\a-sen\\works\\flask')
#
# for value in sys.path:
#     print(value)

from sqlalchemy import Column, Integer, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from lib.setting import engine, base, session


class Message(base):
    """
    メッセージモデルc
    ユーザーが投稿したメッセージをこのモデルで管理する
    """

    __tablename__ = 'messages'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "メッセージモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="メッセージID")
    message = Column(Text(), nullable=False, comment="メッセージ")
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False, comment="ルームID")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment="ユーザーID")

    # created_at = Column(Date, nullable=True, comment="作成日時")
    # deleted_at = Column(Date, nullable=True, comment="削除日時")

if __name__ == "__main__":
    # テーブル作成
    base.metadata.create_all(engine)
    messages = session.query(Message.message).all()
    print(messages)
    for message in messages:
        print(message.message)
    pass
