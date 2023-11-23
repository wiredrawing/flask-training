from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint, Date, DateTime, func
from sqlalchemy.orm import relationship
from lib.setting import session, base, engine


class MessageLike(base):
    __tablename__ = 'message_likes'

    __table_args__ = (
        (UniqueConstraint('user_id', 'message_id', name='unique_user_id_message_id')),
        {
            'mysql_collate': 'utf8_general_ci',
            "comment": "メッセージモデル",
        })

    id = Column(Integer, primary_key=True, autoincrement=True, comment="メッセージID")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment="ユーザーID")
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False, comment="メッセージID")
    # func.now()はサーバーのデフォルト値を設定する場合
    created_at = Column(DateTime, nullable=False, comment="いいねした日時", default=func.now())
    deleted_at = Column(DateTime, nullable=True, comment="いいねを取り消した日時", default=func.now());

    user = relationship("User", back_populates="message_likes")
    message = relationship("Message", back_populates="message_likes")
