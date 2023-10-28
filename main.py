import time

from flask import Flask, request, make_response, render_template, jsonify;

app = Flask(__name__, template_folder="templates")


# TOPページ
@app.route('/')
def hello():
    return "Hello World!"


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


if __name__ == "__main__":
    app.run(debug=True)

# # これはサンプルの Python スクリプトです。
#
# # Shift+F10 を押して実行するか、ご自身のコードに置き換えてください。
# # Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。
#
#
# def print_hi(name):
#     # スクリプトをデバッグするには以下のコード行でブレークポイントを使用してください。
#     print(f'Hi, {name}')  # Ctrl+F8を押すとブレークポイントを切り替えます。
#
#
# # ガター内の緑色のボタンを押すとスクリプトを実行します。
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
