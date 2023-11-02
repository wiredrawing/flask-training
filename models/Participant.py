from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from lib.setting import session, base, engine



class Participant(base):
    __tablename__ = 'participants'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "参加者モデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="参加者ID")
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, comment="ルームID")
    # users.idを外部キーに設定
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="ユーザーID")

    # belongs_toの場合 => back_populates で関連付けると動作する
    # user = relationship("User", back_populates="participants")


if __name__ == "__main__":
    base.metadata.create_all(engine)
    participants = session.query(Participant).all()
    for participant in participants:
        print(participant.user_id);
        pass
