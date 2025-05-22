import sqlite3
import csv
import os

# テーブルの中身が存在しない場合に実行してください


def csv2table():
    # games.dbを作成し、接続（すでに存在する場合は接続のみ）
    con = sqlite3.connect("instance/gamedb.sqlite")
    cur = con.cursor()
    # csvファイルの指定
    csv_paths = os.listdir("data/csv")
    for csv_path in csv_paths:
        name = csv_path.split("_")[0]  # csvファイル名からテーブル名を取得
        data = open(f"data/csv/{csv_path}", encoding="utf-8")
        # csvファイルを読み込む
        read_csv = csv.reader(data)
        # next()関数を用いて最初の行(列名)はスキップさせる
        next_row = next(read_csv)
        # csvデータをINSERTする
        rows = []
        for row in read_csv:
            rows.append(row)
        # executemany()で複数のINSERTを実行する
        print("process doing...")
        if name == "base":
            cur.executemany(
                f"INSERT INTO {name}s (appid, name, publisher, short_description, about_the_game) VALUES (?, ?, ?, ?, ?)",
                rows,
            )
        elif name == "image":
            cur.executemany(
                f"INSERT INTO {name}s (appid, capsule, capsule_v5, header, screenshots) VALUES (?, ?, ?, ?, ?)",
                rows,
            )
        elif name == "video":
            cur.executemany(
                f"INSERT INTO {name}s (appid, name, thumbnail, video_480p, video_max) VALUES (?, ?, ?, ?, ?)",
                rows,
            )
        # テーブルの変更内容保存
        data.close()
    # データベースの接続終了
    con.commit()
    con.close()
    print("process done.")


if __name__ == "__main__":
    csv2table()
