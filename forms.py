from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectMultipleField, widgets
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
        validators=[
            DataRequired("パスワードは必須入力です"),
            Length(4, 10, "パスワードの長さは4文字以上10文字以内で入力してください"),
        ],
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


# JSONファイルから選択した経験価値の観点を読み込む関数
def load_viewpoint_choices():
    json_path = "/data/nagao/game_rec/data/json/viewpoint_qwen3.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    group_choices = {}
    for main_group_name, main_group in data.items():
        if main_group_name not in group_choices:
            group_choices[main_group_name] = {}
        for subgroup_name, viewpoints in main_group.items():
            group_choices[main_group_name][subgroup_name] = [(id, label) for label, id in viewpoints.items()]

    return group_choices


# チェックボックスを複数選択するためのフィールド
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ol", prefix_label=False)
    option_widget = widgets.CheckboxInput()


# ゲーム検索用フォームを生成する関数
def generate_game_form(viewpoint_choices):
    class DynamicGameForm(FlaskForm):
        title = StringField("ゲームタイトル：")
        submit = SubmitField("検索")

    # 大グループごとにサブグループ単位でフィールド追加
    for main_group, subgroups in viewpoint_choices.items():
        for subgroup, choices in subgroups.items():
            field = MultiCheckboxField(f"{main_group} - {subgroup}", coerce=int, choices=choices)
            # フィールド名例: vp_SENSE_graphics
            setattr(DynamicGameForm, f"vp_{main_group}_{subgroup}", field)
    return DynamicGameForm
