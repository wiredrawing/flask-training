from datetime import datetime
from logging import getLogger, handlers, DEBUG, FileHandler, StreamHandler, INFO, Formatter


def get_app_logger(logger_name: str):
    try:
        # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
        app_logger = getLogger()
        # ロガー自体にログレベルを設定しておく
        app_logger.setLevel(DEBUG)

        today = datetime.now().strftime("%Y-%m-%d")
        # 全体のログ設定

        # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
        rotating_handler = handlers.RotatingFileHandler(
            # ※注意)プログラム実行ディレクトリのlogs/app.logに出力
            r'./logs/{}.app.log.{}'.format(logger_name, today),
            mode="a",
            maxBytes=1000 * 1024 * 1024 * 1024,
            backupCount=10,
            encoding="utf-8"
        )
        rotating_handler.setFormatter(Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s'));
        rotating_handler.setLevel(INFO)

        # コンソール出力用のハンドラーを作成する
        stream_handler = StreamHandler();
        stream_handler.setLevel(DEBUG)
        stream_handler.setFormatter(Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s'));

        if app_logger.hasHandlers() is False:
            app_logger.addHandler(rotating_handler)
            app_logger.addHandler(stream_handler)
        return app_logger
    except Exception as e:
        print(e)
        return None
