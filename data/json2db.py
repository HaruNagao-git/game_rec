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
                all_sql = (
                    insert_sql + "(appid, name, publisher, short_description, about_the_game) VALUES (?, ?, ?, ?, ?)"
                )
                for title, obj in data.items():
                    rows.append(
                        [
                            obj["appid"],
                            title,
                            json.dumps(obj["publisher"], ensure_ascii=False),
                            obj["short_description"],
                            obj["about_the_game"],
                        ]
                    )
            elif info_name == "image":
                all_sql = insert_sql + "(appid, capsule, capsule_v5, header, screenshots) VALUES (?, ?, ?, ?, ?)"
                for obj in data:
                    rows.append(
                        [
                            obj["appid"],
                            obj["capsule"],
                            obj["capsule_v5"],
                            obj["header"],
                            json.dumps(obj["screenshots"], ensure_ascii=False),
                        ]
                    )
            elif info_name == "video":
                all_sql = insert_sql + "(appid, name, thumbnail, video_480p, video_max) VALUES (?, ?, ?, ?, ?)"
                for appid in data:
                    for video in data[appid]:
                        rows.append(
                            [int(appid), video["name"], video["thumbnail"], video["video_480p"], video["video_max"]]
                        )

            cur.executemany(all_sql, rows)

    # jsonファイルの指定
    json_paths = "data/json/aspect_word2vec.json"
    with open(json_paths, "r", encoding="utf-8") as f:
        data = json.load(f)

        # jsonデータをINSERTする
        rows = []
        for exp in data:
            for aspect in data[exp]:
                rows.append([exp, aspect])
        # executemany()で複数のINSERTを実行する
        print("inserting aspect data...")
        cur.executemany(
            "INSERT INTO aspects (experience, name) VALUES (?, ?)",
            rows,
        )

    entity_path = "data/json/entity_word2vec.json"
    with open(entity_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        # jsonデータをINSERTする
        rows = []
        for appid in data:
            for exp in data[appid]:
                for i in range(len(data[appid][exp])):
                    if "aspect" in data[appid][exp][i]:
                        aspect = data[appid][exp][i]["aspect"]
                        aspect_id = cur.execute(
                            "SELECT aspect_id FROM aspects WHERE experience = ? AND name = ?", (exp, aspect)
                        ).fetchone()
                        rows.append([appid, aspect_id[0]])

        # executemany()で複数のINSERTを実行する
        print("inserting base_aspects data...")
        cur.executemany(
            "INSERT INTO base_aspects (appid, aspect_id) VALUES (?, ?)",
            rows,
        )

    # データベースの接続終了
    con.commit()
    con.close()
    print("process done.")


if __name__ == "__main__":
    json2table()
