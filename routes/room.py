from flask import Flask, Blueprint, render_template, redirect, request
from flask_login import current_user

from lib.setting import session
from models.Message import Message
from models.Room import Room

app = Blueprint('room', __name__, url_prefix='/room')


@app.route("/", methods=['GET'])
def index():
    # ログインしていない場合はログインページにリダイレクト
    # 要ログイン
    if current_user.is_authenticated is not True:
        return redirect("/login")
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
