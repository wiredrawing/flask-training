import bcrypt
from flask import Blueprint, render_template, request, make_response, Flask, session as http_session, redirect
from flask_login import current_user, login_user

from lib.setting import session
from models.User import User

app = Blueprint('login_user', __name__, url_prefix='/login')


# ログインフォーム
@app.route("/", methods=['GET'])
def login():
    try:
        # print("current_user.is_authenticated ====>");
        # print(current_user.is_authenticated)
        # if current_user.is_authenticated:
        #     return redirect("/dashboard")

        print("まだログインしていません");
        # print(current_user)
        # print(current_user.id)
        # print(current_user.username);
        # print(current_user.email);
        # print(current_user.password)
        return render_template("login/login.html")
    except Exception as e:
        print(e)
        print(type(e))


@app.route("/authorize", methods=['POST'])
def authorize():
    try:
        # Fetch the post_data converted to a dictionary
        post_data = request.form.to_dict()
        if "email" in post_data:
            user = session.query(User).filter(User.email == post_data["email"]).first()
            if user is None:
                raise Exception("認証処理に失敗しました")
            # end
            
            hashed_password = bcrypt.checkpw(post_data["password"].encode("utf-8"), user.password.encode("utf-8"))
            if hashed_password is not True:
                raise Exception("認証処理に失敗しました")
            # end
            
            # http_session.permanent = True
            # # セッションにオブジェクトをまるごと入れることはできないみたい
            # http_session["user_id"] = user.id
            # print(http_session)

            result = login_user(user, True)
            if result is not True:
                raise Exception("認証処理に失敗しました")

            # ダッシュボードにリダイレクト(ログイン後のマイページ)
            return redirect("/dashboard")

        pass
    except Exception as e:
        print(type(e))
        print(e);
        return redirect("/login")
