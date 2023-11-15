from datetime import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint, Date, DateTime, func
from sqlalchemy.orm import relationship

from lib.setting import session, base, engine


class Participant(base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="参加者ID")
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, comment="ルームID")
    # users.idを外部キーに設定
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="ユーザーID")

    created_at = Column(DateTime, nullable=False, comment="作成日時", default=func.now())
    updated_at = Column(DateTime, nullable=False, comment="更新日時", default=func.now())

    # belongs_toの場合 => back_populates で関連付けると動作する
    # user = relationship("User", back_populates="participants")
    room = relationship("Room", )

    # 複数のカラムでユニークキーを設定する場合は、UniqueConstraintを使う
    __table_args__ = (
        (UniqueConstraint('room_id', 'user_id', name='unique_room_id_user_id')),
        {
            'mysql_collate': 'utf8_general_ci',
            "comment": "参加者モデル",
        })

if __name__ == "__main__":
    base.metadata.create_all(engine)
    participants = session.query(Participant).all()
    for participant in participants:
        print(participant.user_id);
        pass
