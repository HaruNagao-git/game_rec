from flask import render_template, redirect, url_for, Blueprint, session, request
from flask_login import login_required
from forms import generate_game_form, load_viewpoint_choices
import json
from math import ceil
from models import Base, Image, Video, Review, Viewpoint, BaseViewpoint, db
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
        if not title:
            # すべての大グループ・サブグループのフィールドから値を取得
            for main_group, subgroups in viewpoint_choices.items():
                for subgroup in subgroups:
                    field_name = f"vp_{main_group}_{subgroup}"
                    field_data = getattr(form, field_name).data
                    if field_data:
                        viewpoints.extend(field_data)

        # viewpointsをセッションに保存
        query = title if title else "viewpoints"
        # "viewpoints"の場合、選択した観点をセッションに保存
        if query == "viewpoints":
            session["viewpoints"] = viewpoints
        elif "viewpoints" in session:
            session.pop("viewpoints", None)

        # 前回の検索結果をセッションから削除
        if "query" in session:
            session.pop("query", None)
        if "games" in session:
            session.pop("games", None)
        if "games_page" in session:
            session.pop("games_page", None)

        # 画面遷移
        return redirect(url_for("game.index", query=query))
    # GETメソッドの場合
    return render_template("game/search_form.html", form=form, viewpoint_choices=viewpoint_choices)


# Viewpointオブジェクトを辞書に変換
def viewpoint_to_dict(vp):
    return {
        "vp_id": vp.vp_id,
        "main_group": vp.main_group,
        "subgroup": vp.subgroup,
        "viewpoint": vp.sim_group,
    }


def paginate_list(items, page, per_page):
    total = len(items)
    total_pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages


# 検索結果一覧
@game_bp.route("/index/<query>")
@login_required
def index(query):
    # ページ番号取得
    page = int(request.args.get("page", 1))
    per_page = 10  # 1ページあたりの件数

    # セッションから観点情報を取得
    # もしセッションに保存されていなければ空の辞書を使用
    viewpoints = session.get("viewpoints", {})
    # 一致するゲーム情報を全取得
    title = query
    games = []

    # viewpointsが空でない場合、選択した観点が存在するゲーム情報を中間テーブルbase_viewpointsから取得
    if viewpoints:
        # viewpointsリストに含まれる観点IDを取得
        viewpoint_objs = Viewpoint.query.filter(Viewpoint.vp_id.in_(viewpoints)).all()
        viewpoint_ids = [a.vp_id for a in viewpoint_objs]

        # BaseViewpointからappidごとに一致数をカウントし、多い順に並べる
        base_viewpoints = (
            db.session.query(Base, func.count(BaseViewpoint.vp_id).label("match_count"))
            .join(BaseViewpoint, Base.appid == BaseViewpoint.appid)
            .filter(BaseViewpoint.vp_id.in_(viewpoint_ids))
            .group_by(Base.appid)
            .order_by(desc("match_count"))
        )
        for base, _ in base_viewpoints.all():
            # Imageテーブルからの情報を取得
            images = Image.query.filter(Image.appid == base.appid).first()

            # そのゲームが持つ観点ID一覧
            game_viewpoint_ids = [bv.vp_id for bv in BaseViewpoint.query.filter_by(appid=base.appid).all()]
            # 選択した観点のうち、そのゲームが持つものだけ抽出
            game_viewpoint_ids = [bv.vp_id for bv in BaseViewpoint.query.filter_by(appid=base.appid).all()]
            matched_viewpoints = [viewpoint_to_dict(v) for v in viewpoint_objs if v.vp_id in game_viewpoint_ids]

            games.append(
                {
                    "query": query,
                    "appid": base.appid,
                    "name": base.name,
                    "short_description": base.short_description,
                    "header": images.header,
                    "matched_viewpoints": matched_viewpoints,
                }
            )
        games.sort(key=lambda g: len(g["matched_viewpoints"]), reverse=True)
    else:
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
                    "matched_viewpoints": [],
                }
            )

    # 検索結果をセッションに保存
    session["query"] = query

    # ページネーション
    games_page, total_pages = paginate_list(games, page, per_page)

    # 画面遷移
    return render_template("game/index.html", games=games_page, page=page, total_pages=total_pages, query=query)


# 検索結果の詳細
@game_bp.route("/result/<query>/<int:appid>")
@login_required
def result(appid, query):
    # セッションに保存したデータから，matched_viewpointsを取得
    viewpoints = session.get("viewpoints", {})
    matched_viewpoints = []
    if viewpoints:
        viewpoint_objs = Viewpoint.query.filter(Viewpoint.vp_id.in_(viewpoints)).all()
        game_viewpoint_ids = [bv.vp_id for bv in BaseViewpoint.query.filter_by(appid=appid).all()]
        matched_viewpoints = [viewpoint_to_dict(v) for v in viewpoint_objs if v.vp_id in game_viewpoint_ids]

    # APPIDに一致するゲーム情報を取得
    base = Base.query.get_or_404(appid)
    images = Image.query.filter(Image.appid == base.appid).first()
    videos = Video.query.filter(Video.appid == base.appid).all()
    base_review_vps = (
        BaseViewpoint.query.join(Viewpoint, BaseViewpoint.vp_id == Viewpoint.vp_id)
        .join(Review, BaseViewpoint.review_id == Review.review_id)
        .filter(BaseViewpoint.appid == base.appid)
        .all()
    )

    # screenshotsのJSON文字列をリストに変換
    screenshots_338p = json.loads(images.screenshots) if images and images.screenshots else []
    screenshots_1080p = json.loads(images.screenshots_full) if images and images.screenshots_full else []
    screenshots = (
        [
            {"338p": screenshot_338p, "1080p": screenshot_1080p}
            for screenshot_338p, screenshot_1080p in zip(screenshots_338p, screenshots_1080p)
        ]
        if screenshots_338p
        else []
    )

    # videoの情報を整理
    videos_data = [{"480p": v.video_480p, "1080p": v.video_max} for v in videos]

    review_exp = {}
    for brv in base_review_vps:
        if any(mv["viewpoint"] == brv.viewpoint.sim_group for mv in matched_viewpoints):
            if brv.review_id not in review_exp:
                review_exp[brv.review_id] = {"text": brv.review.review_text, "vp_list": []}
            review_exp[brv.review_id]["vp_list"].append(
                {
                    "main_group": brv.viewpoint.main_group,
                    "sim_group": brv.viewpoint.sim_group,
                    "viewpoint": brv.vp_name,
                    "evaluation": brv.evaluation,
                    "eval_sentence": brv.eval_sentence,
                }
            )

    game = {
        "query": query,
        "appid": base.appid,
        "name": base.name,
        "publisher": base.publisher,
        "short_description": base.short_description,
        "about_the_game": base.about_the_game,
        "header": images.header,
        "screenshots": screenshots,
        "thumbnails": [v.thumbnail for v in videos],
        "videos": videos_data,
        "review_exp": review_exp,
    }
    # 画面遷移
    return render_template("game/result.html", game=game)
