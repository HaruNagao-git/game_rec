from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Memo


# ==============================================================================
# Formクラス
# ==============================================================================
# メモ用入力クラス
class MemoForm(FlaskForm):
    # タイトル
    title = StringField(
        "タイトル：",
        validators=[DataRequired("タイトルは必須入力です"), Length(max=50, message="50文字以内で入力してください")],
    )
    # 内容
    content = TextAreaField("内容：")
    # 送信ボタン
    submit = SubmitField("送信")

    # タイトルの重複チェック
    def validate_title(self, title):
        # StringFieldのdata属性で入力値を取得
        memo = Memo.query.filter_by(title=title.data).first()
        # タイトルが重複していないかチェック
        if memo:
            raise ValidationError(f"タイトル'{title.data}'は既に存在します。別のタイトルを入力してください")
