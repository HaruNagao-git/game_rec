from os import urandom


# ==============================================================================
# 設定
# ==============================================================================
class Config(object):
    # デバッグモード
    DEBUG = True
    # CSRFやセッションで使用
    SECRET_KEY = urandom(24)
    # 警告対策
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # データベースの設定
    SQLALCHEMY_DATABASE_URI = "sqlite:///gamedb.sqlite"
