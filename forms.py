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
    file_path = "data/json/aspect_word2vec.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        aspects = []
        for key, value in data[exp].items():
            aspects.append((value, key))
            
        return aspects

    return False


# チェックボックスを複数選択するためのフィールド
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ol", prefix_label=False)
    option_widget = widgets.CheckboxInput()


# ゲーム検索用入力クラス
class GameForm(FlaskForm):
    # ゲームタイトル
    title = StringField("ゲームタイトル：")
    
    # 経験的価値の観点
    asp_sense = MultiCheckboxField("SENSE", choices=load_aspect("SENSE"), coerce=int)
    asp_feel = MultiCheckboxField("FEEL", choices=load_aspect("FEEL"), coerce=int)
    asp_think = MultiCheckboxField("THINK", choices=load_aspect("THINK"), coerce=int)
    asp_act = MultiCheckboxField("ACT", choices=load_aspect("ACT"), coerce=int)
    asp_relate = MultiCheckboxField("RELATE", choices=load_aspect("RELATE"), coerce=int)

    # 検索ボタン
    submit = SubmitField("検索")
    
    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False
        # すべて未入力かを確認
        if not self.title.data and not (
            self.asp_sense.data or
            self.asp_feel.data or
            self.asp_think.data or
            self.asp_act.data or
            self.asp_relate.data
        ):
            error_message = f"{self.asp_sense.data} ゲームタイトルまたは１つ以上の観点を入力してください"
            self.title.errors.append(error_message)  # 適当なフィールドにエラーを出す
            return False

        return True
