# Steamゲーム推薦システム
バーンド・H・シュミットの経験価値をレビューから抽出し，観点として選択できるようにしたSteamゲーム推薦システムです．

## 使い方
まず、githubからこのプロジェクトをクローンします。以下のコマンドを実行します。

1. ```git clone https://github.com/HaruNagao-git/game_rec.git```

### 研究室の計算機にクローンした場合
仮想環境は構築しなくて大丈夫です．

### 手元のanacondaを使用しているPCにクローンした場合
クローンしたプロジェクトフォルダまで移動＆condaで仮想環境を作成し、アクティブ状態にします。以下のコマンドを実行します。

2. ```cd game_rec```
3. ```conda create -n game_rec python==3.12.8```
4. ```conda activate game_rec```

```install_packages.txt```からアプリケーションを動かすのに必要なパッケージをインストールします。以下のコマンドを実行します(※少々時間がかかります)。

5. ```conda install --file install_packages.txt```

### アプリを起動
```app.py```を実行し、出力される以下のテキストの```Running on ...```のURL部分をアクセスするとログイン画面が表示されます。（手元のPCにクローンした方はgame_rec環境をアクティベートしてください．）

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
* Debugger PIN: 355-361-532
```

ここまで出来たら，あとは適当なユーザ名とパスワードでサインアップをしてからログインをしてください．
