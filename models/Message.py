from datetime import datetime

# sys.path.append('C:\\Users\\a-sen\\works\\flask')
#
# for value in sys.path:
#     print(value)

from sqlalchemy import Column, Integer, Text, ForeignKey, Date, DateTime, func
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
    # サーバーのデフォルト値を設定する場合
    # func.now()を設定する
    created_at = Column(DateTime, nullable=False, comment="作成日時", default=func.now())
    updated_at = Column(DateTime, nullable=False, comment="更新日時", default=func.now())
    deleted_at = Column(DateTime, nullable=False, comment="削除日時", default=func.now())

    user = relationship("User", order_by="User.id.asc()", back_populates="messages")
    room = relationship("Room", back_populates="messages")

if __name__ == "__main__":
    # テーブル作成
    base.metadata.create_all(engine)
    messages = session.query(Message.message).all()
    print(messages)
    for message in messages:
        print(message.message)
    pass
