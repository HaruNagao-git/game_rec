from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from models import Game
from forms import GameForm
from flask_login import login_required
import ast

# memoのBlueprintを作成
game_bp = Blueprint("game", __name__, url_prefix="/game")


# ==============================================================================
# ルーティング
# ==============================================================================
# APPIDによる検索(Formを使用)
@game_bp.route("/", methods=["GET", "POST"])
@login_required
def search():
    # フォームの生成
    form = GameForm()
    # POSTメソッドの場合
    if request.method == "POST" and form.validate():
        # フォームの入力値を取得
        appid = form.appid.data
        # 画面遷移
        return redirect(url_for("game.index", appid=appid))
    # GETメソッドの場合
    return render_template("game/search_form.html", form=form)


# 検索結果一覧
@game_bp.route("/index/<int:appid>")
@login_required
def index(appid):
    # 一致するゲーム情報を全取得
    games = Game.query.filter(Game.appid == appid).all()
    # 画面遷移
    return render_template("game/index.html", games=games)


# 検索結果の詳細
@game_bp.route("/result/<int:appid>")
@login_required
def result(appid):
    # APPIDに一致するゲーム情報を取得
    game = Game.query.get_or_404(appid)
    # videos, thumbnailsを辞書型に変換
    game.videos = ast.literal_eval(game.videos)
    game.thumbnails = ast.literal_eval(game.thumbnails)
    # 画面遷移
    return render_template("game/result.html", game=game, appid=appid)


# javaScriptからのリクエストに対応
@game_bp.route("/get_video", methods=["POST"])
def get_video():
    videoid = request.json.get("videoid")
    appid = request.json.get("appid")
    game = Game.query.get_or_404(appid)
    videos = ast.literal_eval(game.videos)
    video = videos[videoid]
    return jsonify(video)
