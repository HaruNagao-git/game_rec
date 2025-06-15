import ast
from flask import render_template, redirect, url_for, Blueprint, session, request
from flask_login import login_required
from forms import GameForm
from models import Base, Image, Video, Aspect, BaseAspect, db
from sqlalchemy import func, desc

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
    form = GameForm(request.form)
    # POSTメソッドの場合
    if form.validate_on_submit():
        # テキストフォームの入力値を取得
        title = form.title.data
        # チェックボックスフォームの入力値を取得
        # 入力値をリスト型にまとめる
        aspects = []
        if form.asp_sense.data:
            aspects.extend(form.asp_sense.data)
        if form.asp_feel.data:
            aspects.extend(form.asp_feel.data)
        if form.asp_think.data:
            aspects.extend(form.asp_think.data)
        if form.asp_act.data:
            aspects.extend(form.asp_act.data)
        if form.asp_relate.data:
            aspects.extend(form.asp_relate.data)
        # aspectsをセッションに保存
        session["aspects"] = aspects
        query = title if title else "aspects"
        # 画面遷移
        return redirect(url_for("game.index", query=query))
    # GETメソッドの場合
    return render_template("game/search_form.html", form=form)


# 検索結果一覧
@game_bp.route("/index/<query>")
@login_required
def index(query):
    # セッションから観点情報を取得
    # もしセッションに保存されていなければ空の辞書を使用
    aspects = session.get("aspects", {})
    # 一致するゲーム情報を全取得
    title = query
    # aspectsが空でない場合、選択した観点が存在するゲーム情報を中間テーブルbase_aspectsから取得
    if aspects:
        # aspectsリストに含まれる観点IDを取得
        aspect_objs = Aspect.query.filter(Aspect.aspect_id.in_(aspects)).all()
        aspect_ids = [a.aspect_id for a in aspect_objs]

        # BaseAspectからappidごとに一致数をカウントし、多い順に並べる
        base_aspects = (
            db.session.query(
                Base,
                func.count(BaseAspect.aspect_id).label("match_count")
            )
            .join(BaseAspect, Base.appid == BaseAspect.appid)
            .filter(BaseAspect.aspect_id.in_(aspect_ids))
            .group_by(Base.appid)
            .order_by(desc("match_count"))
            .limit(10)  # 上位10件を取得
        )
    if title != "aspects":
        # タイトルがある場合は、Baseテーブルからタイトルに一致するゲーム情報を取得
        base_aspects = (
            db.session.query(Base)
            .filter(Base.name.ilike(f"%{title}%"))
        )
    
    games = []
    for base, match_count in base_aspects.all():
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
