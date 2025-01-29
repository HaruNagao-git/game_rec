from flask import Flask
from flask_migrate import Migrate
from models import db

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

# views.pyの読み込み
from views import *

# ==============================================================================
# 実行
# ==============================================================================
if __name__ == "__main__":
    app.run()
