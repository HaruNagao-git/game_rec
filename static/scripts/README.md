# JavaScript

`game_rec` のフロント側UI（動画/画像表示，レビュー表示，フォーム補助など）を制御するスクリプト群です．主にjQueryを使用しています．

## 前提となる大域データ
テンプレート側で以下が定義されている前提の実装が含まれます．
- `gameInfo`：ゲーム詳細（`videos` / `thumbnails` / `screenshots` / `about_the_game` / `review_exp` 等）
- `desktopImgPath` / `mobileImgPath`：ログイン背景画像パス（`card_background.js`）

また，`variables.js` / `base.js` が `thumbList`・`videoList`・`$video`・`$player` 等を初期化し，他ファイルから参照されます．

## 各ファイルの役割
- `variables.js`
    - `gameInfo` からサムネ/動画/スクショ配列を組み立て，説明文（`.description`）を反映します．
- `media.js`
    - サムネイル（動画＋スクショ）のスライダーを生成し，クリックでメイン表示（動画/画像）を切り替えます．
    - 動画/画像のプリロード，カレントスライドの見切れ補正スクロールも行います．
- `base.js`
    - カスタム動画プレイヤーの再生/一時停止，ホバー時のコントロール自動非表示，キーボードショートカット（`k/f/m/j/l`・矢印）を提供します．
    - `window.currentVideoIndex` / `window.currentQuality` を保持します．
- `time_control.js`
    - 10秒送り/戻し，シークバー（進捗）更新，マウスオーバー時の時間インジケーター表示を担当します．
- `volume_control.js`
    - 音量バーの変更とアイコン（ミュート/通常）切替，ホバー時の音量バー表示制御を担当します．
- `fullscreen.js`
    - 全画面ボタンでのフルスクリーン切替と，状態に応じた `.fullscreen` クラスの付け外しを行います．
- `definition_setting.js`
    - 歯車メニューから画質（例：`480p`/`1080p`）を切り替え，再生位置・再生/停止状態を維持してソースを差し替えます．
- `modal_window.js`
    - スクリーンショットのモーダル表示と，前後移動・ページ番号表示を担当します．
- `link_review.js`
    - レビュー文中の「評価文に一致する部分」をリンク化し，クリック時にその箇所に対応する観点情報（グループ/観点名/該当文）をパネル内へ表示します．
- `viewpoint-area.js`
    - 観点（チェックボックス）の選択状態を「選択済み一覧」に反映します．
    - 観点/サブグループにホバーした際に説明文を表示します（説明辞書は `vp2Desc.js` 側）．
- `vp2Desc.js`
    - サブグループ/類似グループの説明辞書（`subgroupDesc` / `simGroupDesc`）を定義します．
    - ファイル先頭コメントにある通り，生成済みJSONから内容をコピペ更新する運用を想定しています．
- `accordion.js`
    - `details/summary` を使ったアコーディオンの開閉アニメーションと，「閉じる」ボタン処理を担当します．
- `index_panel.js`
    - 画面幅に応じたゲーム名の省略表示，matched_viewpoints の表示量制御を行います．
    - インデックスパネルのスクロール位置を `sessionStorage` に保存/復元します．
- `nav_anime.js`
    - モバイル向けメニューの開閉（ボタン文言 `Menu`/`Close` 切替）を行います．
- `pagination.js`
    - ページネーションの「前へ/次へ」を無効状態（`.disabled`）に応じて抑止しつつ，基本はサーバーサイド遷移に任せます．
- `card_background.js`
    - ログイン画面の背景画像を，画面幅に応じてPC/モバイル用に切り替えます．
- `toggle_visible.js`
    - `input[type="password"]` に「表示/非表示」トグルボタン（SVG）を付与し，パスワードの可視化を行います．