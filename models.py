from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Flask-SQLAlchemyの生成
db = SQLAlchemy()


# ==============================================================================
# モデルの定義
# ==============================================================================
# メモ
class Memo(db.Model):
    # テーブル名
    __tablename__ = "memos"
    # ID(PK)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # タイトル(NULLを許可しない)
    title = db.Column(db.String(50), nullable=False)
    # 内容
    content = db.Column(db.Text)


# ユーザ
class User(UserMixin, db.Model):
    # テーブル名
    __tablename__ = "users"
    # ID(PK)
    id = db.Column(db.Integer, primary_key=True)
    # ユーザ名(NULLを許可しない)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # パスワード(NULLを許可しない)
    password = db.Column(db.String(120), nullable=False)

    # パスワードのハッシュ化
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # パスワードの照合
    def check_password(self, password):
        return check_password_hash(self.password, password)


# ゲーム情報
# class Game(db.Model):
#     # テーブル名
#     __tablename__ = "games"
#     # APPID(PK)
#     appid = db.Column(db.Integer, primary_key=True)
#     # ゲームタイトル(NULLを許可しない)
#     name = db.Column(db.String(50), nullable=False)
#     # ゲーム発売元
#     publisher = db.Column(db.String(50))
#     # ゲーム詳細
#     short_description = db.Column(db.Text)
#     # 映像のリンク
#     videos = db.Column(db.Text)
#     # サムネイルのリンク
#     thumbnails = db.Column(db.Text)
