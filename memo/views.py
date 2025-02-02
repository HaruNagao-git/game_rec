from flask import render_template, redirect, url_for, flash, Blueprint, request
from models import db, Memo
from forms import MemoForm
from flask_login import login_required

# memoのBlueprintを作成
memo_bp = Blueprint("memo", __name__, url_prefix="/memo")


# ==============================================================================
# ルーティング
# ==============================================================================
# 一覧表示
@memo_bp.route("/")
@login_required
def index():
    # メモ全件取得
    memos = Memo.query.all()
    # 画面遷移
    return render_template("memo/index.html", memos=memos)


# 新規作成(Formクラスを使用)
@memo_bp.route("/create", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("memo.index"))
    else:
        # 画面遷移
        return render_template("memo/create_form.html", form=form)


# 更新(Formクラスを使用)
@memo_bp.route("/update/<int:memo_id>", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("memo.index"))
    # GETメソッドの場合
    else:
        # 画面遷移
        return render_template("memo/update_form.html", form=form, edit_id=target_data.id)


# 削除
@memo_bp.route("/delete/<int:memo_id>")
@login_required
def delete(memo_id):
    # メモを取得, 存在しない場合は404エラーを返す
    memo = Memo.query.get_or_404(memo_id)
    # データベースから削除
    db.session.delete(memo)
    db.session.commit()
    # フラッシュメッセージを設定
    flash("メモを削除しました")
    # 一覧画面にリダイレクト
    return redirect(url_for("memo.index"))
