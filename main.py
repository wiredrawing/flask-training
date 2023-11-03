# from datetime import time
import time
from flask import Flask, request, make_response, render_template, jsonify, Blueprint
from sqlalchemy.orm import Session

from lib.setting import session, engine
from models.Participant import Participant
from models.Room import Room
from models.User import User
from models.Message import Message

# 自作外部ファイルルーティングをimport
from routes import register_user

app = Flask(__name__, template_folder="templates")
app.register_blueprint(register_user.app)


@app.route("/loop")
def loop():
    def inner():
        # 無限ループでServer Sent Eventを実行する
        while True:
            yield "これは無限ループのSSEエンドポイントです{}{}".format("\n", "\n")
            time.sleep(1)

    response = make_response(inner())
    response.headers["Content-Type"] = "text/event-stream; charset=UTF-8"
    return response


# TOPページ
@app.route('/')
def hello():
    # DB接続のテスト
    messages = session.query(Message.message).all()
    for message in messages:
        print(message)

    params = {
        "template_title": "flask test",
        "template_message": "ここにテンプレートに渡す値を設定する"
    }
    return render_template("index.html", **params)


@app.route("/test/get", methods=['GET'])
def get_method():
    # フォームhtml
    return render_template('form.html', title="flask test", message="Hello World!")


# POSTメソッド フォームからの値を取得
# POSTメソッド フォームからの値を取得
@app.route('/test/post', methods=['POST'])
def post_method():
    request_data = request.form
    body = request_data.to_dict()
    # main contents is set to response.data;
    # htmlテンプレートのレンダリング結果をレスポンスbodyに設定
    response = make_response(render_template('post.html', body=body))
    response.headers['X-Something'] = 'header value goes here'
    response.headers["add-original-header"] = "This is original header.";
    return response


# server sent eventを動作させる場合は以下のように実装する
@app.route("/api/v1/users", methods=['GET'])
def api_users():
    def sse_response():
        for value in range(1000):
            yield f"data: 現在の値 => {value}\n\n"
            time.sleep(1)
        pass

    response = make_response(sse_response())
    response.headers["Content-Type"] = "text/event-stream; charset=UTF-8"
    return response


@app.route("/add/somedata/to/db", methods=['GET'])
def add_somedata_to_db():
    # 何かしらユーザーデータを登録する
    user = User();
    user.username = "testuser"
    user.gender = 1;
    session.add(user)
    session.commit()

    def inner():
        # 新規データを登録後,全レコードを取得する
        users = session.query(User).all()
        for user in users:
            yield f"data: {user.username}\n\n"
            time.sleep(1)
        pass

    inner_variable = inner

    # トランザクションを使用した場合
    try:
        session.begin()
        transaction_user = User()
        transaction_user.username = "transaction_user"
        transaction_user.gender = 2
        session.add(transaction_user)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    # server sent eventでレコードを垂れ流してみる
    response = make_response(inner_variable())
    response.headers["Content-Type"] = "text/event-stream; charset=UTF-8"
    return response


# scoped_sessionを使わない場合
@app.route("/just/in/time/add", methods=['GET'])
def just_in_time_add():
    session = Session(engine)
    try:
        session.begin();
        room = Room();
        room.room_name = "★ここは40代男性のみのルームです";
        room.description = "★40代男性のみのルームです";
        session.add(room)
        session.commit();
    except Exception as e:
        session.rollback();

    rooms = session.query(Room).all()

    def inner():
        for room in rooms:
            yield f"data: {room.room_name}\n\n"
            time.sleep(1)
        pass

    response = make_response(inner());
    response.headers["Content-Type"] = "text/event-stream; charset=UTF-8"
    return response


@app.route("/login", methods=['GET'])
def login():
    print("チャットルームに対する参加者を取得する")
    participants = session.query(Participant).filter(Participant.id == 1).first()
    if participants:
        print("participantsテーブルに該当レコードが存在します")
        print(participants);
        print(participants.user.id)
        print(participants.user.email)
        print(participants.user.password)
        print(participants.user.username)
        pass
    else:
        print("participantsテーブルに該当レコードが存在しません")
        pass

    print("Userモデルからみた関係");
    user = session.query(User).filter(User.id == 2).first()
    if user:
        print(user)
        print(user.participants)
        for p in user.participants:
            print(participants.id)
            print(participants.room_id)
            print(participants.user_id)
    response = make_response(render_template("login/login.html"))
    return response


@app.route("/login/authorize", methods=['POST'])
def authorize():
    # formから入力されたアカウント情報を取得
    request_data = request.form
    body = request_data.to_dict()
    print(body)
    # テストアプリケーションのため平文で検証
    user = session.query(User).filter(User.email == body["email"]) \
        .filter(User.password == body["password"]).first()
    if user != None:
        print(user.participants)
        for participant in user.participants:
            print(participant.room_id)
            print(participant.user_id)
            print(participant.id);
        # ログイン成功
        return "ログインしました"
    return "ログインに失敗しました"


@app.route("/add/message", methods=['GET'])
def add_message_form():
    return render_template("message/add_form.html")


@app.route("/add/message", methods=['POST'])
def add_message():
    try:
        # フォームからメッセージを取得
        request_data = request.form
        body = request_data.to_dict()
        print(body)
        # メッセージを登録
        message = Message()
        message.message = body["message"]
        message.room_id = 1
        message.user_id = 1
        session.add(message)
        session.commit()
    except Exception as e:
        session.rollback();
        print(e);
        return "メッセージの送信に失敗しました"

    return "メッセージを登録しました"


if __name__ == "__main__":
    app.run(debug=True)
