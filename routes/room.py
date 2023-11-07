from flask import Flask, Blueprint, render_template, redirect, request
from flask_login import current_user

from lib.setting import session
from models.Message import Message
from models.Room import Room
from logging import LogRecord, LoggerAdapter, getLogger, handlers
import logging

app = Blueprint('room', __name__, url_prefix='/room')


try:
    # 全体のログ設定
    # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
    root_logger = getLogger()
    root_logger.setLevel(logging.ERROR)
    rotating_handler = handlers.RotatingFileHandler(
        # ※注意)プログラム実行ディレクトリのlogs/app.logに出力
        r'./logs/app.log',
        mode="a",
        maxBytes=100 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    format = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
    rotating_handler.setFormatter(format)
    root_logger.addHandler(rotating_handler)
except Exception as e:
    print(e);


@app.route("/", methods=['GET'])
def index():
    logger = getLogger(__name__)
    logger.debug("あああああああああああああ");
    # ログインしていない場合はログインページにリダイレクト
    # 要ログイン
    if current_user.is_authenticated is not True:
        return redirect("/login")
    # end
    print(current_user.password)
    # 現在稼働中のチャットルーム一覧を表示
    rooms = session.query(Room).all()
    """現在,作成されているチャットルーム一覧を表示"""
    return render_template("room/index.html", rooms=rooms)


@app.route("/<int:room_id>", methods=['GET'])
def room(room_id):
    if current_user.is_authenticated is not True:
        return redirect("/login")
    print(current_user)
    print(current_user.get_id())
    print("current_user.id ===> {}".format(current_user.id))
    print(dir(current_user))
    print("current_user.id ===> {}".format(current_user.id))

    room = session.query(Room).filter(Room.id == room_id).first()
    print(dir(room))
    """指定されたチャットルームに紐づくメッセージを表示"""
    return render_template("room/room.html", room=room, user=current_user, messages=room.messages)


@app.route("/message/create/<int:room_id>", methods=['POST'])
def create_message(room_id):
    try:
        required_keys = [
            "user_id",
            "message",
        ]
        post_data = request.form.to_dict()

        # 正しいpostデータの場合はメッセージを登録
        if required_keys == list(post_data.keys()):
            message = Message()
            message.message = post_data["message"]
            message.room_id = room_id
            message.user_id = post_data["user_id"]
            session.add(message)
            session.commit()
            pass

        return "";
    except Exception as e:
        print(e)

    return ""
