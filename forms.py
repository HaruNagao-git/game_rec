from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Base, User


# ==============================================================================
# Formクラス
# ==============================================================================
# ログイン用入力クラス
class LoginForm(FlaskForm):
    # ユーザ名
    username = StringField(
        "ユーザ名：",
        validators=[DataRequired("ユーザ名は必須入力です")],
    )
    # パスワード
    password = PasswordField(
        "パスワード：",
        validators=[Length(4, 10, "パスワードの長さは4文字以上10文字以内で入力してください")],
    )
    # 送信ボタン
    submit = SubmitField("ログイン")

    # カスタムバリデータ
    # 英数字と記号が含まれているかチェックする
    def validate_password(self, password):
        # 英数字と記号が含まれているかチェック
        if not (
            any(c.isalpha() for c in password.data)
            and any(c.isdigit() for c in password.data)
            and any(c in "!@#$%^&*()" for c in password.data)
        ):
            raise ValidationError("パスワードは【英数字と記号：!@#$%^&*()】を含めてください")


# サインアップ用入力クラス
class SignUpForm(LoginForm):
    # ボタン
    submit = SubmitField("サインアップ")

    # カスタムバリデータ
    def validate_username(self, username):
        # ユーザ名が既に登録されていないかチェック
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"ユーザ名'{username.data}'は既に存在します。別のユーザ名を入力してください")


# ゲーム検索用入力クラス
class GameForm(FlaskForm):
    # APPID
    appid = IntegerField(
        "APPID：",
        validators=[DataRequired("IDは必須入力です")],
    )
    # 検索ボタン
    submit = SubmitField("検索")

    # カスタムバリデータ
    def validate_game(self, appid):
        # APPIDに対応しているゲームが登録されているかチェック
        game = Base.query.filter(appid=appid.data).all()
        if not game:
            raise ValidationError(f"APPID'{appid.data}'のゲームは存在しません。別のAPPIDを入力してください")
