import bcrypt
from flask import Blueprint, render_template, request, redirect

from lib.MakeRandomToken import MakeRandomToken
from lib.logger import get_app_logger
from lib.setting import session
from models.User import User
from routes.CreateUserForm import CreateUserForm

app = Blueprint('register_user', __name__, url_prefix='/user')


# 参考URL: https://qiita.com/miyakiyo/items/34617adaf77acf8b4511
# 新規ユーザー登録のルーティング
@app.route("/register/", methods=['GET'])
def register():
    form = CreateUserForm(request.form)
    print(form);
    print(form.email.data)
    print(MakeRandomToken().token(40))
    return render_template("user/register.html", form=form)


@app.route("/register/", methods=['POST'])
def post_register():
    try:
        form = CreateUserForm(request.form)
        print("------------------------------------------------")
        if form.validate() is not True:
            get_app_logger(__name__).error(form.errors)
            return render_template("user/register.html", form=form)

        print(form)
        # 辞書型に変換してPOSTデータを取得する
        post_data = request.form.to_dict()
        print(post_data)
        token = MakeRandomToken().token(40)
        user = User()
        user.email = post_data["email"]
        user.username = post_data["username"]
        user.gender = post_data["gender"]
        user.zipcode = post_data["zipcode"]
        user.address = post_data["address"]
        user.phone_number = post_data["phone_number"]
        user.token = token
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
        return redirect("/user/register/completed/" + token)
    except Exception as e:
        get_app_logger(__name__).error(e)
    return ""


@app.route("/register/completed/<string:token>", methods=['GET'])
def register_completed(token: str):
    """ユーザー登録完了画面"""
    return render_template("user/register_completed.html")
