from datetime import datetime
from logging import getLogger, handlers
import logging

# ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
app_logger = getLogger()
# ログレベルを設定しておく
app_logger.setLevel(logging.ERROR)
app_logger.setLevel(logging.INFO)
app_logger.setLevel(logging.DEBUG)
app_logger.setLevel(logging.WARNING)

def get_app_logger():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        # 全体のログ設定

        rotating_handler = handlers.RotatingFileHandler(
            # ※注意)プログラム実行ディレクトリのlogs/app.logに出力
            r'./logs/app.log.{}'.format(today),
            mode="a",
            maxBytes=500 * 1024,
            backupCount=10,
            encoding="utf-8"
        )
        app_logger.addHandler(rotating_handler)
        return app_logger
    except Exception as e:
        print(e)
        return None
