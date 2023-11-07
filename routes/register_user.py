import bcrypt
from flask import Blueprint, render_template, request, redirect

from lib.setting import session
from models.User import User

app = Blueprint('register_user', __name__, url_prefix='/user')


# 参考URL: https://qiita.com/miyakiyo/items/34617adaf77acf8b4511
# 新規ユーザー登録のルーティング
@app.route("/register", methods=['GET'])
def register():
    return render_template("user/register.html")


@app.route("/register", methods=['POST'])
def post_register():
    try:
        # 辞書型に変換してPOSTデータを取得する
        post_data = request.form.to_dict()
        print(post_data)
        user = User()
        user.email = post_data["email"]
        user.username = post_data["username"]
        user.gender = post_data["gender"]
        # blowfishでハッシュ化する
        # saltの生成
        salt = bcrypt.gensalt(rounds=12, prefix=b"2a")
        hashed_password = bcrypt.hashpw(post_data["password"].encode("utf-8"), salt).decode("utf-8")
        user.password = hashed_password
        # ユーザーを登録
        session.add(user)
        session.commit();
        print("ユーザー登録完了")
        print(user.id)
        # ログインページにリダイレクト
        return redirect("/login")
    except Exception as e:
        print(e)
    return ""
