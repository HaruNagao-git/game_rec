import sqlite3
import json

# テーブルの中身が存在しない場合に実行してください

def json2table():
    # games.dbを作成し、接続（すでに存在する場合は接続のみ）
    con = sqlite3.connect("instance/gamedb.sqlite")
    cur = con.cursor()

    # jsonファイルの指定
    json_paths = "data/json/aspect_word2vec.json"
    with open(json_paths, "r", encoding="utf-8") as f:
        data = json.load(f)
        
        # jsonデータをINSERTする
        rows = []
        for exp in data:
            for aspect in (data[exp]):
                rows.append([exp, aspect])
        # executemany()で複数のINSERTを実行する
        print(f"inserting aspect data...")
        cur.executemany(
            f"INSERT INTO aspects (experience, name) VALUES (?, ?)",
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
        print(f"inserting base_aspects data...")
        cur.executemany(
            f"INSERT INTO base_aspects (appid, aspect_id) VALUES (?, ?)",
            rows,
        )

    # データベースの接続終了
    con.commit()
    con.close()
    print("process done.")


if __name__ == "__main__":
    json2table()