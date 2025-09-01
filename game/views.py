from flask import render_template, redirect, url_for, Blueprint, session, request
from flask_login import login_required
from forms import generate_game_form, load_viewpoint_choices
import json
from models import Base, Image, Video, Viewpoint, BaseViewpoint, db
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
    viewpoint_choices = load_viewpoint_choices()
    form = generate_game_form(viewpoint_choices)(request.form)
    # POSTメソッドの場合
    if form.validate_on_submit():
        # テキストフォームの入力値を取得
        title = form.title.data
        # チェックボックスフォームの入力値を取得
        # 入力値をリスト型にまとめる
        viewpoints = []
        # すべての大グループ・サブグループのフィールドから値を取得
        for main_group, subgroups in viewpoint_choices.items():
            for subgroup in subgroups:
                field_name = f"vp_{main_group}_{subgroup}"
                field_data = getattr(form, field_name).data
                if field_data:
                    viewpoints.extend(field_data)
        # viewpointsをセッションに保存
        session["viewpoints"] = viewpoints
        query = title if title else "viewpoints"
        # 画面遷移
        return redirect(url_for("game.index", query=query))
    # GETメソッドの場合
    return render_template("game/search_form.html", form=form, viewpoint_choices=viewpoint_choices)


# 検索結果一覧
@game_bp.route("/index/<query>")
@login_required
def index(query):
    # セッションから観点情報を取得
    # もしセッションに保存されていなければ空の辞書を使用
    viewpoints = session.get("viewpoints", {})
    # 一致するゲーム情報を全取得
    title = query
    games = []
    # viewpointsが空でない場合、選択した観点が存在するゲーム情報を中間テーブルbase_viewpointsから取得
    if viewpoints:
        # viewpointsリストに含まれる観点IDを取得
        viewpoint_objs = Viewpoint.query.filter(Viewpoint.viewpoint_id.in_(viewpoints)).all()
        viewpoint_ids = [a.viewpoint_id for a in viewpoint_objs]

        # BaseViewpointからappidごとに一致数をカウントし、多い順に並べる
        base_viewpoints = (
            db.session.query(Base, func.count(BaseViewpoint.viewpoint_id).label("match_count"))
            .join(BaseViewpoint, Base.appid == BaseViewpoint.appid)
            .filter(BaseViewpoint.viewpoint_id.in_(viewpoint_ids))
            .group_by(Base.appid)
            .order_by(desc("match_count"))
            .limit(10)  # 上位10件を取得
        )
        for base, _ in base_viewpoints.all():
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
    if title != "viewpoints":
        # タイトルがある場合は、Baseテーブルからタイトルに一致するゲーム情報を取得
        base_viewpoints = db.session.query(Base).filter(Base.name.ilike(f"%{title}%"))
        for base in base_viewpoints.all():
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
        "screenshots": json.loads(images.screenshots),
        "thumbnails": [v.thumbnail for v in videos],
        "videos_max": [v.video_max for v in videos],
    }
    # 画面遷移
    return render_template("game/result.html", game=game)
