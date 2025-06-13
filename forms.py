from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, ValidationError
from models import User
import json


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


# JSONファイルから選択した経験的価値の観点を読み込む関数
def load_aspect(exp=None):
    file_path = "data/aspect.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        aspects = [(aspect, aspect) for i, aspect in enumerate(data[exp])]
        return aspects

    return False


# チェックボックスを複数選択するためのフィールド
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ol", prefix_label=False)
    option_widget = widgets.CheckboxInput()


# ゲーム検索用入力クラス
class GameForm(FlaskForm):
    # APPID
    appid = IntegerField("APPID：")
    # ゲームタイトル
    title = StringField("ゲームタイトル：")
    # 検索ボタン
    submit = SubmitField("検索")
    # 経験的価値の観点
    asp_sense = MultiCheckboxField("SENSE", choices=load_aspect("SENSE"), coerce=str)
    asp_feel = MultiCheckboxField("FEEL", choices=load_aspect("FEEL"), coerce=str)
    asp_think = MultiCheckboxField("THINK", choices=load_aspect("THINK"), coerce=str)
    asp_act = MultiCheckboxField("ACT", choices=load_aspect("ACT"), coerce=str)
    asp_relate = MultiCheckboxField("RELATE", choices=load_aspect("RELATE"), coerce=str)

    # カスタムバリデータ
    def validate_appid(self, field):
        # APPIDが未入力の場合（ただしtitleも未入力の時のみ）
        if not field.data and not self.title.data:
            raise ValidationError("APPIDまたはゲームタイトルを入力してください")
        # APPIDが数字以外の値が入力された場合のエラー
        if field.data is not None and not isinstance(field.data, int):
            raise ValidationError("APPIDは数字で入力してください")

    def validate_title(self, field):
        # ゲームタイトル未入力の場合のエラー（ただしAPPIDも未入力の時のみ）
        if not field.data and not self.appid.data:
            raise ValidationError("APPIDまたはゲームタイトルを入力してください")
