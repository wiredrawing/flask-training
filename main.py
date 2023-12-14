# from datetime import time
import configparser
import redis
from datetime import timedelta

from flask import Flask, request, make_response, render_template, jsonify, Blueprint, session as http_session, redirect
from flask_login import current_user, LoginManager, decode_cookie, encode_cookie
from sqlalchemy.orm import Session
from werkzeug import Response

from lib.logger import get_app_logger
from lib.setting import session, engine
from models.Participant import Participant
from models.Room import Room
from models.User import User
from models.Message import Message

# 自作外部ファイルルーティングをimport
from routes import register_user, sse, message_like
from routes import login_user
from routes import dashboard
from routes import room
from routes import api
from routes.admin.index import app as admin
from app import app

# app = Flask(__name__, template_folder="templates")

# 外部ファイルに指定したルーティング処理を登録する
app.register_blueprint(register_user.app)
app.register_blueprint(login_user.app)
app.register_blueprint(dashboard.app)
app.register_blueprint(room.app)
app.register_blueprint(sse.app)
app.register_blueprint(api.app)
app.register_blueprint(message_like.app)
app.register_blueprint(admin)
app.secret_key = "random seckey for flask"
app.permanent_session_lifetime = timedelta(days=365)


class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)


app.wsgi_app = Middleware(app.wsgi_app)


# @app.route("/loop")
# def loop():
#     def inner():
#         # 無限ループでServer Sent Eventを実行する
#         while True:
#             yield "これは無限ループのSSEエンドポイントです{}{}".format("\n", "\n")
#             time.sleep(1)
#
#     response = make_response(inner())
#     response.headers["Content-Type"] = "text/event-stream; charset=UTF-8"
#     return response


# TOPページ
@app.route('/')
def hello():
    # DB接続のテスト
    messages = session.query(Message.message).all()
    for message in messages:
        pass
        # print(message)

    user = session.query(User).filter(User.id == current_user.id).first()
    if user is None:
        raise Exception("ユーザーが存在しません")
    # end

    params = {
        "template_title": "flask test",
        "template_message": "ここにテンプレートに渡す値を設定する",
        "current_user": current_user,
        "user": user,
    }
    # print(user.messages)
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


@app.route("/message/add", methods=['GET'])
def add_message_form():
    user_id = http_session.get("user_id");
    if user_id is None:
        return "ログインしてください"

    return render_template("message/add_form.html")


@app.route("/message/add", methods=['POST'])
def add_message():
    user_id = http_session.get("user_id");
    if user_id is None:
        return "ログインしてください"
    try:
        # フォームからメッセージを取得
        request_data = request.form
        body = request_data.to_dict()

        # メッセージは必須とする
        if len(body["message"]) == 0:
            return "メッセージを入力してください"
        # print(body)
        # メッセージを登録
        message = Message()
        message.message = body["message"]
        message.room_id = 1
        message.user_id = user_id
        session.add(message)
        session.commit()
    except Exception as e:
        session.rollback();
        get_app_logger().error(e)
        # print(e);
        return "メッセージの送信に失敗しました"

    return "メッセージを登録しました"


# 指定したルーティング以外は認証を必須とする
# もし非認証だった場合はログインページにリダイレクトする
@app.before_request
def hook() -> Response | None:
    if request.path.find("/sse") != -1 or request.path.find("/api") != -1:
        return None
    # ログインフォーム以外はログイン済みであることを確認する
    if (request.path.find("/login")) != -1 or (request.path.find("/user/register")) != -1:
        # ログインフォームは非認証状態でもアクセス可能
        return None

    if current_user.is_authenticated is not True:
        return redirect("/login")
    else:
        pass
    return None


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
