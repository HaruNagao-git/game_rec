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
# ヘルプページ
@game_bp.route("/help", methods=["GET"])
@login_required
def help():
    viewpoint_choices = load_viewpoint_choices()
    form = generate_game_form(viewpoint_choices)(request.form)
    return render_template("game/help.html", form=form, viewpoint_choices=viewpoint_choices)


# タイトル，観点による検索(Formを使用)
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

        # 画面遷移
        return redirect(url_for("game.index", query=query, index=1))
    # GETメソッドの場合
    return render_template("game/search_form.html", form=form, viewpoint_choices=viewpoint_choices)


# ページネーション処理
def paginate_list(items, page, per_page):
    total = len(items.all())
    total_pages = ceil(total / per_page)
    start = (page - 1) * per_page
    return items.offset(start).limit(per_page), total_pages


# 検索結果一覧
@game_bp.route("/index/<query>/<int:index>", methods=["GET"])
@login_required
def index(query, index):
    # ページ番号取得
    page = int(request.args.get("page", 1))
    per_page = 10  # 1ページあたりの件数

    # セッションから観点情報を取得
    # もしセッションに保存されていなければ空の辞書を使用
    viewpoints = session.get("viewpoints", {})
    # 一致するゲーム情報を全取得
    title = query
    game_list = []
    # viewpointsが空でない場合、選択した観点が存在するゲーム情報を中間テーブルbase_viewpointsから取得
    if viewpoints:
        # BaseViewpointからappidごとに一致数をカウントし、多い順に並べる
        base_viewpoints = (
            db.session.query(Base, func.count(BaseViewpoint.vp_id))
            .join(BaseViewpoint, Base.appid == BaseViewpoint.appid)
            .filter(BaseViewpoint.vp_id.in_(viewpoints))
            .group_by(Base.appid)
            .order_by(desc(func.count(BaseViewpoint.vp_id)))
            .limit(30)  # 上位30件まで取得
        )

        # ページネーション
        base_viewpoints, total_pages = paginate_list(base_viewpoints, page, per_page)

        for base, vp_count in base_viewpoints.all():
            # Imageテーブルからの情報を取得
            images = fetch_image_info(base)
            # 一致する観点情報を取得
            matched_viewpoints = fetch_matched_viewpoints(viewpoints, base)
            videos = fetch_video_info(base)
            review_exp = fetch_review_info(base, matched_viewpoints)
            game_list.append(
                {
                    "appid": base.appid,
                    "name": base.name,
                    "matched_viewpoints": matched_viewpoints,
                    "publisher": base.publisher,
                    "short_description": base.short_description,
                    "about_the_game": base.about_the_game,
                    "header": images["header"],
                    "screenshots": images["screenshots"],
                    "thumbnails": videos["thumbnails"],
                    "videos": videos["videos"],
                    "review_exp": review_exp,
                }
            )
    else:
        # タイトルがある場合は、Baseテーブルからタイトルに一致するゲーム情報を取得
        base_viewpoints = db.session.query(Base).filter(Base.name.ilike(f"%{title}%"))

        # ページネーション
        base_viewpoints, total_pages = paginate_list(base_viewpoints, page, per_page)
        for base in base_viewpoints.all():
            # Imageテーブルからの情報を取得
            images = fetch_image_info(base)
            # Videoテーブルからの情報を取得
            videos = fetch_video_info(base)
            game_list.append(
                {
                    "appid": base.appid,
                    "name": base.name,
                    "matched_viewpoints": [],
                    "publisher": base.publisher,
                    "short_description": base.short_description,
                    "about_the_game": base.about_the_game,
                    "header": images["header"],
                    "screenshots": images["screenshots"],
                    "thumbnails": videos["thumbnails"],
                    "videos": videos["videos"],
                    "review_exp": {},
                }
            )

    # 検索結果をセッションに保存
    session["query"] = query

    # 画面遷移
    return render_template(
        "game/index.html", game_list=game_list, page=page, total_pages=total_pages, query=query, index=index
    )


# Viewpointオブジェクトを辞書に変換
def viewpoint_to_dict(vp, vp_count=0):
    return {
        "vp_id": vp.vp_id,
        "vp_count": vp_count,
        "main_group": vp.main_group,
        "subgroup": vp.subgroup,
        "viewpoint": vp.sim_group,
    }


def fetch_matched_viewpoints(viewpoints, base):
    matched_viewpoints = []
    # データベースからそのゲームで一致する観点とその件数を取得
    viewpoints_objs = (
        db.session.query(Viewpoint, func.count(Viewpoint.vp_id))
        .join(BaseViewpoint, Viewpoint.vp_id == BaseViewpoint.vp_id)
        .filter(BaseViewpoint.appid == base.appid, Viewpoint.vp_id.in_(viewpoints))
        .group_by(Viewpoint.vp_id)
    )
    for vo, cnt in viewpoints_objs:
        matched_viewpoints.append(viewpoint_to_dict(vo, cnt))
    return matched_viewpoints


def fetch_image_info(base):
    images = Image.query.filter(Image.appid == base.appid).first()
    if images:
        # screenshotsのJSON文字列をリストに変換
        screenshots_338p = json.loads(images.screenshots) if images and images.screenshots else []
        screenshots_1080p = json.loads(images.screenshots_full) if images and images.screenshots_full else []
        if len(screenshots_338p) == len(screenshots_1080p):
            screenshots = [
                {"338p": screenshot_338p, "1080p": screenshot_1080p}
                for screenshot_338p, screenshot_1080p in zip(screenshots_338p, screenshots_1080p)
            ]
        else:
            screenshots = []
        return {
            "header": images.header,
            "screenshots": screenshots,
        }
    else:
        return {
            "header": None,
            "screenshots": [],
        }


def fetch_video_info(base):
    videos = Video.query.filter(Video.appid == base.appid).all()
    thumbnails = [v.thumbnail for v in videos] if videos else []
    videos_data = [{"480p": v.video_480p, "1080p": v.video_max} for v in videos] if videos else []
    return {
        "thumbnails": thumbnails,
        "videos": videos_data,
    }


def fetch_review_info(base, matched_viewpoints):
    base_review_vps = (
        BaseViewpoint.query.join(Viewpoint, BaseViewpoint.vp_id == Viewpoint.vp_id)
        .join(Review, BaseViewpoint.review_id == Review.review_id)
        .filter(BaseViewpoint.appid == base.appid)
        .all()
    )
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
    return review_exp
