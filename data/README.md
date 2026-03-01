# データベース構築
jsonフォルダ内の各jsonファイルをデータベースに格納する方法を紹介します．

## ファイル構成
```sh
data/
├── json2db.py # jsonファイルからデータベースを構築
├── README.md # このファイル
├── json/ # 規模に依存しないデータ群
│   ├── review_exp.json
│   ├── reviewscore_desc_en2ja.json
│   └── viewpoint_qwen3.json
├── json_lite/ # ゲームデータ群（軽量サイズ）
│   ├── base_info.json
│   ├── image_info.json
│   ├── review_info.json
│   └── video_info.json
└── json_std/ # ゲームデータ群（標準サイズ）
    ├── base_info.json
    ├── image_info.json
    ├── review_info.json
    └── video_info.json
```

## 構築方法
まず，以下のコマンドでSQLiteの初期化をします．

1. `flask db init`

次に，マイグレーションスクリプトを作成するために以下のコマンドを実行します．

2. `flask db migrate`

次に，データベースのスキーマを最新状態にするために，以下のコマンドを実行します．

3. `flask db upgrade`

最後に，以下のコマンドを実行して，`instance/gamedb.sqlite` にデータが記録されていれば完了です．

4. `python3 data/json2db.py --size <std or lite>`


※ `--size`の後に`std`か`lite`を選択し，データベースの規模を指定してください．
- `std`：標準の規模．研究室の計算機など，マシンパワーがある程度大きいPCで展開する場合は，こちらを指定するとよいです．
- `lite`：軽量版の規模．ノートPCなどに展開する場合は，こちらを指定すると良いです．

### データベースを構築し直したい場合
データベースを構築し直したい場合は，2つのディレクトリ `instance/` と `migrations/` を削除し，再度上の手順でコマンドを実行してください．