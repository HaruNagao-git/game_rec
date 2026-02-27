# サーバー構築
本プロジェクトをアプリケーションサーバーとして立ち上げる際に必要になる設定ファイル群です．`gunicorn_template.py`を各自のサーバー環境に適した設定に編集し，`gunicorn.py`として保存してください．

## ファイル構成
```sh
server_settings/
├── (gunicorn.py) # gunicorn_template.pyを編集したもの
└── gunicorn_template.py
```