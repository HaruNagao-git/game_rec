from flask import render_template, redirect, url_for
from app import app

# 循環インポートを回避するため、エラーハンドリングはここでインポートする
from werkzeug.exceptions import NotFound


# ルートパスへのアクセスはログイン画面へリダイレクト
@app.route("/")
def root():
    return redirect(url_for("auth.login"))


# 404エラーハンドリング
@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    print("エラー内容：", msg)
    return render_template("errors/404.html", msg=msg), 404
