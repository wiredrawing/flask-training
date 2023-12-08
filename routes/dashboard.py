import inspect

import bcrypt
from flask import Flask, Blueprint, session as http_session, render_template, request, redirect
from flask_login import current_user, logout_user
from marshmallow import validate, fields, Schema
from sqlalchemy import text

from lib.setting import session, engine
from models.Room import Room
from models.User import User
from routes.CreateUpdatingPasswordForm import CreateUpdatingPasswordForm, CheckUserExisting, CheckCurrentPassword

app = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@app.route("/", methods=['GET'])
def dashboard():
    room = session.query(Room).filter(Room.id == 1).first()
    print(len(room.messages))
    print(len(Room().messages))
    # print(len(Room.messages))

    # print("=============")
    # print(Room())
    # print(Room().messages)
    # print(Room().id)
    # room = Room();
    # print(room.id)
    # print(room.messages)
    # print(room.undefined_value)
    user_id = current_user.id
    user = session.query(User).filter(User.id == user_id).first()
    # 参加しているチャットルーム一覧
    for message in user.messages:
        # print(message.user);
        # print(type(Message.user))
        # print(Message.user.id)
        pass
        # print(message)
        # print(message.id)
        # print(message.message)

    for participant in user.participants:
        pass
        # print(participant.room_id)
        # print(participant.room);
        # print(participant.user)
        # print(participant.room.room_name)
        # print(participant.user.username);
    return render_template("dashboard/dashboard.html", user=user)


@app.route("/edit", methods=['GET'])
def edit():
    """"現在ログインしているユーザーの情報を表示"""
    if "user_id" in http_session:
        user = session.query(User).filter(User.id == http_session["user_id"]).first()
        return render_template("dashboard/edit.html", user=user)
    else:
        return "ログインしてください"


@app.route("/update", methods=['POST'])
def update():
    required_key = [
        "id",
        "email",
        "username",
    ]
    if "user_id" in http_session:
        post_data = request.form.to_dict()
        if required_key == list(post_data.keys()):
            user = session.query(User).filter(User.id == http_session["user_id"]).first()
            user.email = post_data["email"]
            user.username = post_data["username"]
            session.commit()
            return redirect("/dashboard/edit")
    else:
        return "ログインしてください"


# パスワードの更新
@app.route("/password", methods=['GET'])
def password():
    # ログイン中のユーザー情報を取得する
    user_id = current_user.id
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        # ユーザー情報が取得できない場合はログイン画面へ遷移する
        return redirect("/login")
    # ログイン情報を取得した場合パスワード変更画面を表示する
    return render_template("dashboard/password.html", user=user)


@app.route("/password/update", methods=['POST'])
def password_update():
    try:
        post_data = request.form.to_dict()
        users = session.query(User)
        schema = CreateUpdatingPasswordForm()
        """バリデーションルールを実行時に追加していく"""
        # メタクラスによって付与された属性<fields>を都度空っぽにしていく
        for field in list(schema.fields):
            # 空にしないと前回のリクエスト分を保持してしまう
            schema.fields[field].validators = []
            pass
        # ユーザーID
        if not schema.fields["user_id"].validators:
            schema.fields["user_id"].validators.append(
                CheckUserExisting(users, error="ユーザーIDが一致しません")
            )

        # 現在のパスワード
        if not schema.fields["current_password"].validators:
            schema.fields["current_password"].validators.append(
                CheckCurrentPassword(int(post_data["user_id"]), users, error="現在のパスワードが一致しません")
            )
            pass

        # 新規パスワード
        if not schema.fields["new_password"].validators:
            schema.fields["new_password"].validators.append(
                validate.Equal(post_data["new_password_confirm"], error="新しいパスワードと新しいパスワード(確認用)が一致しません(※実行時ルール追加)")
            )
            pass

        # 新規パスワード(確認用)
        if not schema.fields["new_password_confirm"].validators:
            schema.fields["new_password_confirm"].validators.append(
                validate.Equal(post_data["new_password"], error="新しいパスワードと新しいパスワード(確認用)が一致しません(※実行時ルール追加)")
            )
            pass

        # バリデーションエラーを検出
        result = schema.validate(post_data)
        if result != {}:
            for key in list(result):
                print(result[key])
            raise Exception(result);

        # 明示的なトランザクションの開始
        try:
            session.begin(True)
            # パスワードの更新処理を実行する
            user = session.query(User).filter(User.id == post_data["user_id"]).first()
            # blowfishでハッシュ化する
            # saltの生成
            salt = bcrypt.gensalt(rounds=12, prefix=b"2a")
            hashed_password = bcrypt.hashpw(post_data["new_password"].encode("utf-8"), salt).decode("utf-8")
            user.password = hashed_password
            session.commit()

            # 生のSQLを発行する
            sql = text('select connection_id() as connection_id ')
            for row in session.execute(sql):
                print("生SQLの実行結果")
                print(row)
                connection_id = row[0]
                print(f"connection_id => {connection_id}")
            return redirect("/dashboard/password/completed/{}")
        except Exception as e:
            print(e)
            session.rollback();
    except Exception as e:
        print("例外発生-->")
        print(e.args)
        print(e.with_traceback)
        return e


@app.route("/password/completed/<string:completed_hash>", methods=['GET'])
def password_completed(completed_hash: str = ""):
    print(completed_hash)
    return render_template("dashboard/password_completed.html")


# ログアウト処理を実行
@app.route("/logout", methods=['POST'])
def logout():
    if logout_user():
        return redirect("/dashboard")
    else:
        print("ログアウト処理に失敗しました");
