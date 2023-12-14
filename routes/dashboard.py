import inspect

import bcrypt
from flask import Flask, Blueprint, session as http_session, render_template, request, redirect
from flask_login import current_user, logout_user
from marshmallow import validate, fields, Schema
from sqlalchemy import text

from lib.logger import get_app_logger
from lib.setting import session, engine
from models.Room import Room
from models.User import User
from routes.CreateUpdateUserInfoForm import CreateUpdateUserInfoForm
from routes.CreateUpdatingPasswordForm import CreateUpdatingPasswordForm, CheckUserExisting, CheckCurrentPassword

app = Blueprint('dashboard', __name__, url_prefix='/dashboard')


class AppSingleton():

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("インスタンスを新規に作成 ~~~~~~~~~")
            cls._instance = super(AppSingleton, cls).__new__(cls)
            cls._instance.__count = 0;
        return cls._instance

    def __init__(self):
        print("初期化 singleton")
        self.__count += 1;

    @property
    def count(self):
        return self.__count


@app.route("/", methods=['GET'])
def dashboard():
    singleton = AppSingleton()
    print("singleton ====> ", singleton.count)
    singleton2 = AppSingleton()
    print("singleton ====> ", id(singleton))
    print("singleton2 ====> ", id(singleton2))
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
    # 現在ログイン中ユーザー情報を取得
    user_id = current_user.id
    user = session.query(User).filter(User.id == user_id).first()
    schema = CreateUpdateUserInfoForm()

    # バリデータールールを追加する
    # user_id
    schema.fields["id"].validators.append(
        CheckUserExisting(session.query(User), error="ユーザーIDが一致しません")
    )
    # email
    schema.fields["email"].validators.append(
        validate.Email(error="メールアドレスの形式が不正です")
    )
    # username
    schema.fields["username"].validators.append(
        validate.Length(min=4, max=64, error="ユーザー名は1文字以上20文字以下で入力してください")
    )
    # バリデーションエラーを検出
    result = schema.validate(request.form.to_dict())
    if result != {}:
        raise Exception(result)

    try:
        session.begin(True)
        post_data = request.form.to_dict()
        user = session.query(User).filter(User.id == post_data["id"]).first()
        if user is None:
            raise Exception("ユーザーが存在しません")
        user.email = post_data["email"]
        user.username = post_data["username"]
        session.commit()
        # 編集画面へリダイレクト
        return redirect("/dashboard/edit")
    except Exception as e:
        session.rollback();
        get_app_logger(__name__).error(e)
        raise Exception(e)



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
    errors = {};
    return render_template("dashboard/password.html", user=user, errors=errors)


@app.route("/password/update", methods=['POST'])
def password_update():
    try:
        get_app_logger(__name__).info("password_update関数のスタート");
        post_data = request.form.to_dict()
        users = session.query(User)

        # スキーマを生成(おそらくこれはシングルトン)
        schema = CreateUpdatingPasswordForm()
        # schmea2 = CreateUpdatingPasswordForm()

        # members  = inspect.getmembers(CreateUpdatingPasswordForm)
        # for member in members:
        #     print(member)
        #
        #
        # print(CreateUpdatingPasswordForm)
        # print("schema1 => ", id(schema))
        # print("schema2 => ", id(schmea2))
        # get_app_logger(__name__).info("スキーの初期化 {}".format(schema.fields["current_password"].validators))
        """バリデーションルールを実行時に追加していく"""
        # ユーザーID
        schema.fields["user_id"].validators.append(
            CheckUserExisting(users, error="ユーザーIDが一致しません")
        )

        # 現在のパスワード
        schema.fields["current_password"].validators.append(
            CheckCurrentPassword(int(post_data["user_id"]), users, error="現在のパスワードが一致しません")
        )

        # 新規パスワード
        schema.fields["new_password"].validators.append(
            validate.Equal(post_data["new_password_confirm"], error="新しいパスワードと新しいパスワード(確認用)が一致しません(※実行時ルール追加)")
        )

        # 新規パスワード(確認用)
        schema.fields["new_password_confirm"].validators.append(
            validate.Equal(post_data["new_password"], error="新しいパスワードと新しいパスワード(確認用)が一致しません(※実行時ルール追加)")
        )

        # バリデーションエラーを検出
        result = schema.validate(post_data)
        if result != {}:
            # バリデーションエラー時
            # 現在ログイン中ユーザの情報を再度テンプレートにわたす
            loggin_user_id = current_user.id
            loggin_user = session.query(User).filter(User.id == loggin_user_id).first()
            get_app_logger(__name__).info(f"バリデーションエラーが発生しました {result}")
            return render_template("dashboard/password.html", user=loggin_user, errors=result)

        try:
            # 明示的なトランザクションの開始
            get_app_logger(__name__).info("--> 明示的なトランザクションの開始")
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
                # 上記のSQL分はMysqlのみで動作する
                return redirect(f"/dashboard/password/completed/{connection_id}")
        except Exception as e:
            get_app_logger(__name__).error(f"例外発生--> ロールバックします {e}")
            session.rollback();
            raise Exception(e)
    except Exception as e:
        get_app_logger(__name__).error(f"例外発生--> {e} テンプレートを返却します")


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
