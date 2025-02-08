import sqlite3
import csv

# gameテーブルが存在しない場合に実行してください


def csv2table():
    # games.dbを作成し、接続（すでに存在する場合は接続のみ）
    con = sqlite3.connect("instance/gamedb.sqlite")
    cur = con.cursor()
    # csvファイルの指定
    open_csv = open("ja_media.csv", encoding="utf-8")
    # csvファイルを読み込む
    read_csv = csv.reader(open_csv)
    # next()関数を用いて最初の行(列名)はスキップさせる
    next_row = next(read_csv)
    # csvデータをINSERTする
    rows = []
    for row in read_csv:
        rows.append(row)
    # executemany()で複数のINSERTを実行する
    cur.executemany(
        "INSERT INTO games (appid, name, publisher, short_description, videos, thumbnails) VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    # テーブルの変更内容保存
    # csvも閉じておきましょう
    con.commit()
    open_csv.close()
    # gamesテーブルの確認
    select_test = "SELECT * FROM games"
    print("—————————-")
    print("fetchall")
    print("—————————-")
    print(cur.execute(select_test))
    print(cur.fetchall())
    # データベースの接続終了
    con.close()


if __name__ == "__main__":
    csv2table()
