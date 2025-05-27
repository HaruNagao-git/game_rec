from flask import render_template, redirect, url_for, Blueprint
from models import Base, Image, Video
from forms import GameForm
from flask_login import login_required
import ast

# gameのBlueprintを作成
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
    if form.validate_on_submit():
        # フォームの入力値を取得
        appid = form.appid.data
        print(appid)
        title = form.title.data
        query = appid if appid else title
        # 画面遷移
        return redirect(url_for("game.index", query=query))
    # GETメソッドの場合
    return render_template("game/search_form.html", form=form)


# 検索結果一覧
@game_bp.route("/index/<query>")
@login_required
def index(query):
    # 一致するゲーム情報を全取得
    if query.isdigit():
        # dataが数字の場合
        appid = int(query)
        bases = Base.query.filter(Base.appid == appid).all()
    else:
        # dataが文字列の場合
        title = query
        bases = Base.query.filter(Base.name.like(f"%{title}%")).all()
    games = []
    for base in bases:
        # Imageテーブルからの情報を取得
        images = Image.query.filter(Image.appid == base.appid).first()
        games.append(
            {
                "query": query,
                "appid": base.appid,
                "name": base.name,
                "short_description": base.short_description,
                "header": images.header,
            }
        )
    # 画面遷移
    return render_template("game/index.html", games=games)


# 検索結果の詳細
@game_bp.route("/result/<query>/<int:appid>")
@login_required
def result(appid, query):
    # APPIDに一致するゲーム情報を取得
    base = Base.query.get_or_404(appid)
    images = Image.query.filter(Image.appid == base.appid).first()
    videos = Video.query.filter(Video.appid == base.appid).all()

    game = {
        "query": query,
        "appid": base.appid,
        "name": base.name,
        "publisher": base.publisher,
        "short_description": base.short_description,
        "about_the_game": base.about_the_game,
        "header": images.header,
        "screenshots": ast.literal_eval(images.screenshots),
        "thumbnails": [v.thumbnail for v in videos],
        "videos_max": [v.video_max for v in videos],
    }
    # 画面遷移
    return render_template("game/result.html", game=game)
