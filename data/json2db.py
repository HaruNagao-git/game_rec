import sqlite3
import json
import os


# テーブルの中身が存在しない場合に実行してください
def json2table():
    # games.dbを作成し、接続（すでに存在する場合は接続のみ）
    con = sqlite3.connect("instance/gamedb.sqlite")
    cur = con.cursor()

    json_paths = [path for path in os.listdir("data/json") if "info" in path]
    for json_path in json_paths:
        # jsonファイルの指定
        info_name = json_path.split("_")[0]
        json_path = os.path.join("data/json", json_path)
        rows = []
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # executemany()で複数のINSERTを実行する
            print(f"inserting {info_name} data from {json_path}...")
            insert_sql = f"INSERT INTO {info_name}s "

            # jsonデータをINSERTする
            if info_name == "base":
                with open("data/json/review_info_tr10.json", "r", encoding="utf-8") as f_review:
                    review_data = json.load(f_review)
                with open("data/json/reviewscore_desc_en2ja.json", "r", encoding="utf-8") as f_review_desc:
                    reviewscore_desc_en2ja = json.load(f_review_desc)
                all_sql = (
                    insert_sql
                    + "(appid, name, publisher, short_description, about_the_game, review_desc_id, review_desc) VALUES (?, ?, ?, ?, ?, ?, ?)"
                )
                for title, obj in data.items():
                    appid = obj["appid"]
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
            elif info_name == "image":
                all_sql = (
                    insert_sql
                    + "(appid, capsule, capsule_v5, header, screenshots, screenshots_full) VALUES (?, ?, ?, ?, ?, ?)"
                )
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
            elif info_name == "video":
                all_sql = insert_sql + "(appid, name, thumbnail, video_480p, video_max) VALUES (?, ?, ?, ?, ?)"
                for appid in data:
                    for video in data[appid]:
                        rows.append(
                            [int(appid), video["name"], video["thumbnail"], video["video_480p"], video["video_max"]]
                        )
            elif info_name == "review":
                all_sql = insert_sql + "(review_id, review_text) VALUES (?, ?)"
                for _, review_obj in data.items():
                    for review in review_obj["reviews"]:
                        rows.append([review["id"], review["text"]])

            cur.executemany(all_sql, rows)

    # jsonファイルの指定
    json_paths = "data/json/viewpoint_qwen3.json"
    with open(json_paths, "r", encoding="utf-8") as f:
        data = json.load(f)

        # jsonデータをINSERTする
        rows = []
        for main_group_name, main_group in data.items():
            for subgroup_name, subgroup in main_group.items():
                for viewpoint_name, _ in subgroup.items():
                    rows.append([main_group_name, subgroup_name, viewpoint_name])
        # executemany()で複数のINSERTを実行する
        print(f"inserting viewpoint data from {json_paths}...")
        cur.executemany(
            "INSERT INTO viewpoints (main_group, subgroup, sim_group) VALUES (?, ?, ?)",
            rows,
        )

    entity_path = "data/json/review_exp.json"
    with open(entity_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        # jsonデータをINSERTする
        rows = []
        viewpoint_id = 0
        for main_group_name, main_group in data.items():
            for subgroup_name, subgroup in main_group.items():
                for viewpoint_name, review_list in subgroup.items():
                    viewpoint_id += 1
                    for review in review_list:
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

        # executemany()で複数のINSERTを実行する
        print(f"inserting base_viewpoints data from {entity_path}...")
        cur.executemany(
            "INSERT INTO base_viewpoints (appid, review_id, vp_id, vp_name, evaluation, eval_sentence) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )

    # データベースの接続終了
    con.commit()
    con.close()
    print("process done.")


if __name__ == "__main__":
    json2table()
