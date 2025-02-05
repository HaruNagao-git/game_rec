from flask import render_template, redirect, url_for, flash, Blueprint
from models import db, User
from forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ==============================================================================
# ルーティング
# ==============================================================================
# ログイン（Form使用）
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    # Formインスタンス使用
    form = LoginForm()
    # POSTメソッドの場合
    if form.validate_on_submit():
        # データ入力取得
        username = form.username.data
        password = form.password.data
        # 対象ユーザ取得
        user = User.query.filter_by(username=username).first()
        # 認証判定
        if user is not None and user.check_password(password):
            # ログイン処理
            login_user(user)
            # ゲーム検索画面にリダイレクト
            return redirect(url_for("game.search"))
        # 失敗
        flash("認証不備です")
    # GETメソッドの場合
    return render_template("auth/login_form.html", form=form)


# ログアウト
@auth_bp.route("/logout")
@login_required
def logout():
    # ログアウト処理
    logout_user()
    # フラッシュメッセージ
    flash("ログアウトしました")
    # ログイン画面にリダイレクト
    return redirect(url_for("auth.login"))


# サインアップ（Form使用）
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Formインスタンス使用
    form = SignUpForm()
    # POSTメソッドの場合
    if form.validate_on_submit():
        # データ入力取得
        username = form.username.data
        password = form.password.data
        # ユーザ新規作成
        user = User(username=username)
        user.set_password(password)
        # データベースに保存
        db.session.add(user)
        db.session.commit()
        # フラッシュメッセージ
        flash("ユーザ登録しました")
        # ログイン画面にリダイレクト
        return redirect(url_for("auth.login"))
    # GETメソッドの場合
    return render_template("auth/register_form.html", form=form)
