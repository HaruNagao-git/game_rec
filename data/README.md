# データベース構築
jsonフォルダ内の各jsonファイルをデータベースに格納する方法を紹介します。

## ファイル構成
```sh
data/
├── json2db.py # jsonファイルからデータベースを構築
├── README.md # このファイル
└── json/ # ゲームデータ群
    ├── base_info.json
    ├── image_info.json
    ├── review_exp.json
    ├── review_info.json
    ├── reviewscore_desc_en2ja.json
    ├── video_info.json
    └── viewpoint_qwen3.json
```

## 構築方法
まず、以下のコマンドでSQLiteの初期化をします。

1. `flask db init`

次に、マイグレーションスクリプトを作成するために以下のコマンドを実行します。

2. `flask db migrate`

次に、データベースのスキーマを最新状態にするために、以下のコマンドを実行します。

3. `flask db upgrade`

最後に、以下のコマンドを実行して、`instance/gamedb.sqlite` にデータが記録されていれば完了です。

4. `python3 data/json2db.py`