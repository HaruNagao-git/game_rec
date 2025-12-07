# gunicornに関する設定ファイルのテンプレート
# このファイルを基に自身のアプリケーションにあわせて編集してください．

wsgi_app = "module:app"  # WSGIアプリケーションのモジュールとアプリケーション名
chdir = "my/working/dir"  # 作業ディレクトリ
bind = "address:port"  # バインドするアドレスとポート
proc_name = "My-Process"  # プロセス名
workers = 1  # ワーカー数
daemon = True  # デーモンモードで起動
reload = True  # ソースコード変更時に自動リロード
accesslog = f"{chdir}/logs/gunicorn_access.log"  # アクセスログの出力先パス("-"は標準出力)
access_log_format = '%(t)s "%(r)s" %(s)s %(b)s "%(f)s"'  # アクセスログのフォーマット
errorlog = f"{chdir}/logs/gunicorn_err.log"  # エラーログの出力先パス("-"は標準出力)
loglevel = "info"  # ログレベル
timeout = 1800  # タイムアウト時間（秒）
