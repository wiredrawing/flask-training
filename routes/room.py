from flask import Flask, Blueprint, render_template, redirect
from flask_login import current_user

from lib.setting import session
from models.Room import Room

app = Blueprint('room', __name__, url_prefix='/room')


@app.route("/", methods=['GET'])
def index():
    # ログインしていない場合はログインページにリダイレクト
    # 要ログイン
    if current_user.is_authenticated is not True:
        return redirect("/login")
    """現在,作成されているチャットルーム一覧を表示"""
    return render_template("room/index.html")


@app.route("/<int:room_id>", methods=['GET'])
def room(room_id):
    room = session.query(Room).filter(Room.id == room_id).first()
    """指定されたチャットルームに紐づくメッセージを表示"""
    return render_template("room/room.html", room=room)
