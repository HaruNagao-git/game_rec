# HTMLテンプレート
Webページを構成するHTMLファイル群です．jinja2を使用して記述しております．

## ファイル構成
```sh
templates/
├── auth_base.html # auth/内HTMLのベースとなるファイル
├── game_base.html # game/内HTMLのベースとなるファイル
├── auth/
│   ├── login_form.html # ログイン画面
│   └── register_form.html # サインアップ画面
├── components/ # Webページの一部を構成する部品
│   ├── card.html # ログイン・サインアップ画面のカードUI
│   ├── checkbox_form.html # 検索画面のチェックボックスフォーム
│   ├── flash.html # フラッシュメッセージ
│   ├── game_result.html # 検索結果画面の詳細情報部分
│   └── text_form.html # 検索画面のゲームタイトル入力フォーム
├── errors/
│   └── 404.html # エラーページ
└── game/
    ├── help.html # ヘルプページ
    ├── index.html # 検索結果画面
    └── search_form.html # 検索画面
```