from flask import Flask, Blueprint, render_template, redirect, request
from flask_login import current_user, login_required

from lib.setting import session
from models.Message import Message
from models.Room import Room
from logging import LogRecord, LoggerAdapter, getLogger, handlers
import logging

app = Blueprint('room', __name__, url_prefix='/room')


def get_app_logger():
    try:
        # 全体のログ設定
        # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
        app_logger = getLogger()
        app_logger.setLevel(logging.ERROR)
        rotating_handler = handlers.RotatingFileHandler(
            # ※注意)プログラム実行ディレクトリのlogs/app.logに出力
            r'./logs/app.log',
            mode="a",
            maxBytes=100 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        app_format = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
        rotating_handler.setFormatter(app_format)
        app_logger.addHandler(rotating_handler)
        return app_logger
    except Exception as e:
        print(type(e))
        print(e)
        return None


#
# with app.app_context_processor() as c:
#     def without_login():
#         logger = get_app_logger()
#         logger.info("ログインしていません")


@app.route("/", methods=['GET'])
# @login_required(without_login)
def index():
    """ログイン状態を必須とする"""
    logger = get_app_logger()
    # logger = getLogger(__name__)
    logger.debug("ロギング処理を関数化して対応");
    logger.error("ロギング処理を関数化して対応")
    print(logger)
    # # ログインしていない場合はログインページにリダイレクト
    # # 要ログイン
    # if current_user.is_authenticated is not True:
    #     return redirect("/login")
    # # end
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
    print(room.messages)
    print(dir(room))
    """指定されたチャットルームに紐づくメッセージを表示"""
    return render_template("room/room.html", room=room, user=current_user, messages=room.messages)


@app.route("/<int:room_id>/message/create/", methods=['POST'])
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
            return redirect("/room/{}".format(room_id))
    except Exception as e:
        print(e)

    return ""


# 新規チャットルームを作成する
@app.route("/add/", methods=['GET'])
def room_form():
    """
    チャットルームを追加する
    :return:
    """
    return render_template("room/add_room.html")


@app.route("/add/", methods=['POST'])
def add_post():
    request_data = request.form
    if len(request_data["room_name"]) == 0 and len(request_data["description"]) == 0:
        return "Room名および概要説明は必須項目です"
    try:
        room_name = request_data["room_name"]
        description = request_data["description"]
        # 同名のルームが存在する場合はエラー
        room_exists = session.query(Room).filter(Room.room_name == room_name).first()
        if (room_exists is not None):
            # 既に存在している場合はそのルームにリダイレクト
            return redirect("/room/{}".format(room_exists.id))
        room = Room();
        room.room_name = room_name
        room.description = description
        session.add(room)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

    # 新規ルームを作成したら
    # 既存ルーム一覧にリダイレクト
    return redirect("/room/")
