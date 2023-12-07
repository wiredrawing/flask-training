import inspect

import bcrypt
from flask import Flask, Blueprint, session as http_session, render_template, request, redirect
from flask_login import current_user, logout_user
from marshmallow import validate, fields, Schema

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
        print(post_data)
        users = session.query(User)
        print(type(users))
        schema = CreateUpdatingPasswordForm()
        # schema = Schema()
        """バリデーションルールを実行時に追加していく"""
        print(dir(schema))
        print(schema.fields)
        # ユーザーID
        if schema.fields["user_id"].validators == []:
            schema.fields["user_id"].validators.append(
                CheckUserExisting(session.query(User), error="ユーザーIDが一致しません")
            )
            pass

        # 現在のパスワード
        # schema.fields["current_password"].validators = []
        if schema.fields["current_password"].validators == []:
            schema.fields["current_password"].validators.append(
                CheckCurrentPassword(int(post_data["user_id"]), session.query(User), error="現在のパスワードが一致しません")
            )
            pass

        # 新規パスワード
        # schema.fields["new_password"].validators = []
        if schema.fields["new_password"].validators == []:
            schema.fields["new_password"].validators.append(
                validate.Equal(post_data["new_password_confirm"], error="新しいパスワードと新しいパスワード(確認用)が一致しません(※実行時ルール追加)")
            )
            pass

        # 新規パスワード(確認用)
        # schema.fields["new_password_confirm"].validators = []
        if schema.fields["new_password_confirm"].validators == []:
            schema.fields["new_password_confirm"].validators.append(
                validate.Equal(post_data["new_password"], error="新しいパスワードと新しいパスワード(確認用)が一致しません(※実行時ルール追加)")
            )
            pass

        result = schema.validate(post_data)
        if result != {}:
            raise Exception(result);
        # パスワードの更新処理を実行する
        user = session.query(User).filter(User.id == post_data["user_id"]).first()
        # blowfishでハッシュ化する
        # saltの生成
        salt = bcrypt.gensalt(rounds=12, prefix=b"2a")
        hashed_password = bcrypt.hashpw(post_data["new_password"].encode("utf-8"), salt).decode("utf-8")
        user.password = hashed_password
        session.commit()
        return redirect("/dashboard/password")
    except Exception as e:
        print(e)
        return e


# ログアウト処理を実行
@app.route("/logout", methods=['POST'])
def logout():
    if logout_user():
        return redirect("/dashboard")
    else:
        print("ログアウト処理に失敗しました");
