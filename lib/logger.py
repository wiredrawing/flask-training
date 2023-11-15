from logging import getLogger, handlers
import logging


def get_app_logger():
    try:
        # 全体のログ設定
        # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
        app_logger = getLogger()
        app_logger.setLevel(logging.ERROR)
        rotating_handler = handlers.RotatingFileHandler(
            # ※注意)プログラム実行ディレクトリのlogs/app.logに出力
            r'./logs/app.log',
            mode="a",
            maxBytes=100 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        app_format = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
        rotating_handler.setFormatter(app_format)
        app_logger.addHandler(rotating_handler)
        return app_logger
    except Exception as e:
        print(type(e))
        print(e)
        return None
