# Steamゲーム推薦システム
Steamゲーム推薦システムの検索機能を、APPIDのみに限定して作成したプロトタイプです。このプロジェクトを軸に、入力を文章にしてBERTによる解析を行ったり、推薦結果を複数並べるように改造する予定です。

## 使い方
まず、githubからこのプロジェクトをクローンします。以下のコマンドを実行します。

1. ```git clone https://github.com/HaruNagao-git/game_rec.git```

次に、クローンしたプロジェクトフォルダまで移動＆condaで仮想環境を作成し、アクティブ状態にします。以下のコマンドを実行します。

2. ```cd game_rec```
3. ```conda create -n game_rec python==3.12.8```
4. ```conda activate game_rec```

```install_packages.txt```からアプリケーションを動かすのに必要なパッケージをインストールします。以下のコマンドを実行します(※少々時間がかかります)。

5. ```conda install --file install_packages.txt```

```app.py```を実行し、出力される以下のテキストの```Running on ...```のURL部分をアクセスするとログイン画面が表示されます。

6. 
```bash
(game_rec) D:\game_rec>python app.py
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: 355-361-532
```

適当なユーザ名とパスワードでログインした後、以下のAPPIDで検索してみてください。
<table>
  <thead>
    <tr>
      <th>APPID</th>
      <th>ゲームタイトル</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1245620</td>
      <td>ELDEN RING</td>
    </tr>
    <tr>
      <td>2552430</td>
      <td>KINGDOM HEARTS -HD 1.5+2.5 ReMIX-</td>
    </tr>
    <tr>
      <td>2909400</td>
      <td>FINAL FANTASY VII REBIRTH</td>
    </tr>
    <tr>
      <td>72850</td>
      <td>The Elder Scrolls V: Skyrim</td>
    </tr>
    <tr>
      <td>570940</td>
      <td>DARK SOULS™: REMASTERED</td>
    </tr>
    <tr>
      <td>921570</td>
      <td>オクトパストラベラー</td>
    </tr>
    <tr>
      <td>2051010</td>
      <td>プロ野球スピリッツ2024-2025</td>
    </tr>
    <tr>
      <td>2280000</td>
      <td>SQUARE ENIX AI Tech Preview: THE PORTOPIA SERIAL MURDER CASE</td>
    </tr>
    <tr>
      <td>2490990</td>
      <td>聖剣伝説 VISIONS of MANA</td>
    </tr>
  </tbody>
</table>

動画や製品詳細のデータが存在すればそれらが表示され、そうでなければ何も表示されません。