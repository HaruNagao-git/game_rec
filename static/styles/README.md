# CSS
Webページの装飾に関するファイル群です．本プロジェクトでは効率化を図り，SCSS（Sassy CSS）を利用しました．

VS CodeでSCSSを利用するには，拡張機能の **DartJS Sass Compiler and Sass Watcher** が必要になります．

## ファイル構成
```sh
styles/
    ├── style.css # 最終的なCSSファイル
    ├── style.min.css # style.cssから空白・改行などを除去してデータ削減したもの（こちらをWebページに読み込ませています）
    ├── style.scss # cssを生成するためのファイル
    ├── bases/ # 各HTMLに共通するスタイルの定義
    │   ├── _base.scss
    │   ├── _common.scss
    │   ├── _variables.scss
    │   ├── _wrapper.scss
    └── pages/ # 各HTMLで独自に必要なスタイルの定義
        ├── _about-game.scss
        ├── _aside.scss
        ├── _card.scss
        ├── _form.scss
        ├── _header.scss
        ├── _help.scss
        ├── _media-panel.scss
        ├── _modal-window.scss
        ├── _review-info.scss
        └── _search-index.scss
```

## 参考文献
1. [1冊ですべて身につくHTML & CSSとWebデザイン入門講座](https://www.amazon.co.jp/1%E5%86%8A%E3%81%A7%E3%81%99%E3%81%B9%E3%81%A6%E8%BA%AB%E3%81%AB%E3%81%A4%E3%81%8FHTML-CSS%E3%81%A8Web%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3%E5%85%A5%E9%96%80%E8%AC%9B%E5%BA%A7-Mana/dp/4797398892/ref=asc_df_4797398892?mcid=e5566912badb38efadc3ce9f87056cec&tag=jpgo-22&linkCode=df0&hvadid=707442440817&hvpos=&hvnetw=g&hvrand=9630474481086267502&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9198318&hvtargid=pla-637663128882&psc=1&hvocijid=9630474481086267502-4797398892-&hvexpln=0)
1. [ほんの一手間で劇的に変わるHTML & CSSとWebデザイン実践講座](https://www.amazon.co.jp/%E3%81%BB%E3%82%93%E3%81%AE%E4%B8%80%E6%89%8B%E9%96%93%E3%81%A7%E5%8A%87%E7%9A%84%E3%81%AB%E5%A4%89%E3%82%8F%E3%82%8BHTML-CSS%E3%81%A8Web%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3%E5%AE%9F%E8%B7%B5%E8%AC%9B%E5%BA%A7-Mana/dp/4815606145/ref=pd_bxgy_d_sccl_2/355-3957010-8363945?pd_rd_w=2AnBG&content-id=amzn1.sym.dee070b1-16ee-44ca-b1c2-031bd9c55b61&pf_rd_p=dee070b1-16ee-44ca-b1c2-031bd9c55b61&pf_rd_r=GYBW35Q6QDCBDHFJ3CS0&pd_rd_wg=WTClI&pd_rd_r=456ec379-f7e8-47e9-a045-9e2f9d34d695&pd_rd_i=4815606145&psc=1)
1. [【Sass】SCSSの基本的な書き方](https://qiita.com/ayumiueda_/items/4edfde9c58f7d87887fc)