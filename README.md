# Steamゲーム推薦システム
B. H. Schmittの経験価値をレビューから抽出し，観点として選択できるようにしたSteamゲーム推薦システムです．

## ファイル構成

```sh
game_rec/
├── app.py # アプリケーション機能に関する重要なプログラム
├── config.py # アプリケーションの設定ファイル
├── forms.py # ブラウザでの入力フォームに関するファイル
├── models.py # データベースの構成に関するファイル
├── requirements.txt # pip環境での必要なライブラリ群
├── requirements conda.txt # conda環境での必要なライブラリ群
├── README.md # このファイル．本プロジェクトの説明．
├── views.py # 開始＆エラーURLのルーティングファイル
...
```

## 使い方
まず，githubからこのプロジェクトをクローンします．以下のコマンドを実行します．

1. ```git clone https://github.com/HaruNagao-git/game_rec.git```

### 研究室の計算機にクローンした場合
仮想環境は構築しなくて大丈夫です．

### 手元のanacondaを使用しているPCにクローンした場合
クローンしたプロジェクトフォルダまで移動後，```conda create```コマンドで仮想環境を作成しアクティブ状態にします．以下のコマンドを実行します．

2. ```cd game_rec```
3. ```conda create -n game_rec python==3.12.8```
4. ```conda activate game_rec```

```requirements_conda.txt```からアプリケーションを動かすのに必要なパッケージをインストールします．以下のコマンドを実行します(※少々時間がかかります)．

5. ```conda install --file requirements_conda.txt```

### アプリを起動
```app.py```を実行し，以下の出力の```Running on ...```以下URLにアクセスするとログイン画面が表示されます．（お手元のPCにクローンした方はgame_rec環境をアクティベートしてください．）

6. 
```bash
user@computer:/game_rec$ python3 app.py
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: xxx-xxx-xxx
```

ここまで出来たら，あとは適当なユーザ名とパスワードでサインアップをしてからログインをしてください．

### 参考文献
- [Flask本格入門 ～やさしくわかるWebアプリ開発～](https://www.amazon.co.jp/Flask%E6%9C%AC%E6%A0%BC%E5%85%A5%E9%96%80-%EF%BD%9E%E3%82%84%E3%81%95%E3%81%97%E3%81%8F%E3%82%8F%E3%81%8B%E3%82%8BWeb%E3%82%A2%E3%83%97%E3%83%AA%E9%96%8B%E7%99%BA%EF%BD%9E-%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%83%95%E3%83%AB%E3%83%8D%E3%82%B9-%E6%A8%B9%E4%B8%8B%E9%9B%85%E7%AB%A0-ebook/dp/B0CDZZYK3H)
    