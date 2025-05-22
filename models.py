from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Flask-SQLAlchemyの生成
db = SQLAlchemy()


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


# ベース情報
class Base(db.Model):
    # テーブル名
    __tablename__ = "bases"
    # APPID(PK)
    appid = db.Column(db.Integer, primary_key=True)
    # ゲームタイトル(NULLを許可しない)
    name = db.Column(db.String(50), nullable=False)
    # ゲーム発売元
    publisher = db.Column(db.String(50))
    # ゲーム概要
    short_description = db.Column(db.Text)
    # ゲームの詳細情報
    about_the_game = db.Column(db.Text)


# 画像情報
class Image(db.Model):
    # テーブル名
    __tablename__ = "images"
    # APPID(PK)
    appid = db.Column(db.Integer, primary_key=True)
    # capsule(URL)
    capsule = db.Column(db.String(200))
    # capsule_v5(URL)
    capsule_v5 = db.Column(db.String(200))
    # header(URL)
    header = db.Column(db.String(200))
    # screenshots(list)
    screenshots = db.Column(db.Text)


# 動画情報
class Video(db.Model):
    # テーブル名
    __tablename__ = "videos"
    # idx(PK)
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # APPID
    appid = db.Column(db.Integer)
    # name
    name = db.Column(db.String(50))
    # thumbnail(URL)
    thumbnail = db.Column(db.String(200))
    # video_480p(URL)
    video_480p = db.Column(db.String(200))
    # video_max(URL)
    video_max = db.Column(db.String(200))
