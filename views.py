from flask import render_template, request, redirect, url_for, flash
from app import app
from models import db, Memo
from forms import MemoForm


# ==============================================================================
# ルーティング
# ==============================================================================
# 一覧表示
@app.route("/memo/")
def index():
    # メモ全件取得
    memos = Memo.query.all()
    # 画面遷移
    return render_template("index.html", memos=memos)


# 新規作成(Formクラスを使用)
@app.route("/memo/create", methods=["GET", "POST"])
def create():
    # フォームの生成
    form = MemoForm()
    # POSTメソッドの場合
    if form.validate_on_submit():
        # フォームの入力値を取得
        title = form.title.data
        content = form.content.data
        # メモを新規作成
        memo = Memo(title=title, content=content)
        # データベースに保存
        db.session.add(memo)
        db.session.commit()
        # フラッシュメッセージを設定
        flash("メモを新規作成しました")
        # 一覧画面にリダイレクト
        return redirect(url_for("index"))
    else:
        # 画面遷移
        return render_template("create_form.html", form=form)


# 更新(Formクラスを使用)
@app.route("/memo/update/<int:memo_id>", methods=["GET", "POST"])
def update(memo_id):
    # メモを取得, 存在しない場合は404エラーを返す
    target_data = Memo.query.get_or_404(memo_id)
    # Formに入れ替え
    form = MemoForm(obj=target_data)

    # POSTメソッドの場合
    if request.method == "POST" and form.validate():
        # フォームの入力値を取得
        target_data.title = form.title.data
        target_data.content = form.content.data
        # データベースに保存
        db.session.commit()
        # フラッシュメッセージを設定
        flash("メモを更新しました")
        # 一覧画面にリダイレクト
        return redirect(url_for("index"))
    # GETメソッドの場合
    else:
        # 画面遷移
        return render_template("update_form.html", form=form, edit_id=target_data.id)


# 削除
@app.route("/memo/delete/<int:memo_id>")
def delete(memo_id):
    # メモを取得, 存在しない場合は404エラーを返す
    memo = Memo.query.get_or_404(memo_id)
    # データベースから削除
    db.session.delete(memo)
    db.session.commit()
    # フラッシュメッセージを設定
    flash("メモを削除しました")
    # 一覧画面にリダイレクト
    return redirect(url_for("index"))


# 循環インポートを回避するため、エラーハンドリングはここでインポートする
from werkzeug.exceptions import NotFound


# 404エラーハンドリング
@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    print("エラー内容：", msg)
    return render_template("errors/404.html", msg=msg), 404
