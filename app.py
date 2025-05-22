from flask import Flask
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager
from auth.views import auth_bp
from game.views import game_bp

# ==============================================================================
# Flask
# ==============================================================================
app = Flask(__name__)
# 設定ファイルの読み込み
app.config.from_object("config.Config")
# dbとFlaskとの紐付け
db.init_app(app)
# マイグレーションの設定
migrate = Migrate(app, db)
# ログインマネージャの設定
login_manager = LoginManager()
# ログインマネージャとFlaskとの紐付け
login_manager.init_app(app)
# ログインが必要なページにアクセスしようとしたときに表示されるメッセージを設定
login_manager.login_message = "認証していません：ログインしてください"
# ログイン後のリダイレクト先(ブループリント対応)
login_manager.login_view = "auth.login"
# ブループリントの登録
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# views.pyの読み込み
from views import *

# ==============================================================================
# 実行
# ==============================================================================
if __name__ == "__main__":
    app.run()
