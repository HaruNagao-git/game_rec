import sqlite3
import json
import os
from pathlib import Path


# JSONファイルを読み込む関数
def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# base_info.jsonのデータを元に、baseテーブルに挿入する行を構築する関数
def build_base_rows(data, base_path):
    review_data = load_json_file(base_path / "review_info.json")
    json_path = Path("data/json/reviewscore_desc_en2ja.json").resolve()
    reviewscore_desc_en2ja = load_json_file(json_path)

    rows = []
    for title, obj in data.items():
        appid = obj["appid"]
        # review_info側のキーは文字列なので、文字列appIDで参照する
        query_summary = review_data[str(appid)]["query_summary"] if str(appid) in review_data else None
        review_desc_id = 0  # レビュー評価IDの初期値
        review_desc_ja = ""  # レビュー評価（日本語）の初期値
        if query_summary:
            review_desc_en = query_summary["review_score_desc"]  # レビュー評価（英語）
            review_desc_id = reviewscore_desc_en2ja[review_desc_en]["score"]
            review_desc_ja = reviewscore_desc_en2ja[review_desc_en]["ja"]
        rows.append(
            [
                appid,
                title,
                json.dumps(obj["publisher"], ensure_ascii=False),
                obj["short_description"],
                obj["about_the_game"],
                review_desc_id,
                review_desc_ja,
            ]
        )

    return rows


# image_info.jsonのデータを元に、imageテーブルに挿入する行を構築する関数
def build_image_rows(data):
    rows = []
    for appid, obj in data.items():
        rows.append(
            [
                int(appid),
                obj["capsule"],
                obj["capsule_v5"],
                obj["header"],
                json.dumps(obj["screenshots"], ensure_ascii=False),
                json.dumps(obj["screenshots_full"], ensure_ascii=False),
            ]
        )
    return rows


# video_info.jsonのデータを元に、videoテーブルに挿入する行を構築する関数
def build_video_rows(data):
    rows = []
    for appid in data:
        for video in data[appid]:
            rows.append([int(appid), video["name"], video["thumbnail"], video["video_480p"], video["video_max"]])
    return rows


# review_info.jsonのデータを元に、reviewテーブルに挿入する行を構築する関数
def build_review_rows(data):
    rows = []
    for _, review_obj in data.items():
        for review in review_obj["reviews"]:
            rows.append([review["id"], review["text"], review["weighted_vote_score"]])
    return rows


# viewpoint_qwen3.jsonのデータを元に、viewpointsテーブルに挿入する関数
def insert_viewpoints(cur):
    json_path = Path("data/json/viewpoint_qwen3.json").resolve()
    data = load_json_file(json_path)

    rows = []
    for main_group_name, main_group in data.items():
        for subgroup_name, subgroup in main_group.items():
            for viewpoint_name, _ in subgroup.items():
                rows.append([main_group_name, subgroup_name, viewpoint_name])

    # 層構造をフラット化してINSERTする
    print(f"inserting viewpoint data from {json_path}...")
    cur.executemany(
        "INSERT INTO viewpoints (main_group, subgroup, sim_group) VALUES (?, ?, ?)",
        rows,
    )


# review_exp.jsonのデータを元に、base_viewpointsテーブルに挿入する関数
def insert_base_viewpoints(cur, base_path):
    entity_path = Path("data/json/review_exp.json").resolve()
    data = load_json_file(entity_path)
    base_info = load_json_file(base_path / "base_info.json")
    appids_lst = [game["appid"] for game in base_info.values()]

    rows = []
    viewpoint_id = 0
    for main_group_name, main_group in data.items():
        for subgroup_name, subgroup in main_group.items():
            for viewpoint_name, review_list in subgroup.items():
                viewpoint_id += 1
                for review in review_list:
                    # base_infoに存在するゲームのレビューだけ処理する
                    if int(review["appid"]) in appids_lst:
                        rows.append(
                            [
                                int(review["appid"]),
                                int(review["id"]),
                                viewpoint_id,
                                review["viewpoint"],
                                review["evaluation"],
                                review["eval_sentence"],
                            ]
                        )

    # appid順にソートする
    rows.sort(key=lambda x: x[0])

    print(f"inserting base_viewpoints data from {entity_path}...")
    cur.executemany(
        "INSERT INTO base_viewpoints (appid, review_id, vp_id, vp_name, evaluation, eval_sentence) VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )


# テーブルの中身が存在しない場合に実行してください
# データの規模モード
# size=std: 標準モード（全データを処理）
# size=lite: 軽量モード（json_liteのデータのみ処理）
def json2table(size="std"):
    # games.dbを作成し、接続（すでに存在する場合は接続のみ）
    con = sqlite3.connect(Path("instance") / "gamedb.sqlite")
    cur = con.cursor()
    base_path = Path(f"data/json_{size}")
    json_paths = [path for path in os.listdir(base_path) if "info" in path]
    for json_path in json_paths:
        # jsonファイルの指定
        info_name = json_path.split("_")[0]
        json_path = base_path / json_path
        data = load_json_file(json_path)

        print(f"inserting {info_name} data from {json_path}...")
        insert_sql = f"INSERT INTO {info_name}s "

        if info_name == "base":
            all_sql = (
                insert_sql
                + "(appid, name, publisher, short_description, about_the_game, review_desc_id, review_desc) VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
            rows = build_base_rows(data, base_path)
        elif info_name == "image":
            all_sql = (
                insert_sql
                + "(appid, capsule, capsule_v5, header, screenshots, screenshots_full) VALUES (?, ?, ?, ?, ?, ?)"
            )
            rows = build_image_rows(data)
        elif info_name == "video":
            all_sql = insert_sql + "(appid, name, thumbnail, video_480p, video_max) VALUES (?, ?, ?, ?, ?)"
            rows = build_video_rows(data)
        elif info_name == "review":
            all_sql = insert_sql + "(review_id, review_text,review_score) VALUES (?, ?, ?)"
            rows = build_review_rows(data)
        else:
            continue

        cur.executemany(all_sql, rows)

    insert_viewpoints(cur)
    insert_base_viewpoints(cur, base_path)

    # データベースの接続終了
    con.commit()
    con.close()
    print("process done.")


if __name__ == "__main__":
    json2table(size="lite")
