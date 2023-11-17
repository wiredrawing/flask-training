from datetime import datetime
from logging import getLogger, handlers
import logging


def get_app_logger():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        # 全体のログ設定
        # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
        app_logger = getLogger()
        # ログレベルを設定しておく
        app_logger.setLevel(logging.ERROR)
        app_logger.setLevel(logging.INFO)
        app_logger.setLevel(logging.DEBUG)
        app_logger.setLevel(logging.WARNING)
        rotating_handler = handlers.RotatingFileHandler(
            # ※注意)プログラム実行ディレクトリのlogs/app.logに出力
            r'./logs/app.log.{}'.format(today),
            mode="a",
            maxBytes=100 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        # app_format = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
        # rotating_handler.setFormatter(app_format)
        app_logger.addHandler(rotating_handler)
        return app_logger
    except Exception as e:
        print(type(e))
        print(e)
        return None
