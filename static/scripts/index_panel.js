'use strict';

// メディアクエリで条件分岐
// 画面幅が768px以上の場合,namesを55文字まで表示
// 画面幅が768px未満の場合,namesを30文字まで表示
//jQueryを使用


$(document).ready(function () {
    function updateDisplay() {
        var isWideScreen = $(window).width() >= 768;
        var nameLength = isWideScreen ? 55 : 30;

        $('.text-area-name').each(function () {
            // 基のテキストをdata属性に保存
            var nameOrigin = $(this).data('name');

            var nameInfo = countChars(nameOrigin, nameLength);
            if (nameInfo.is_long) {
                $(this).text(`${nameOrigin.substring(0, nameInfo.max_idx)}...`);
            }
            else {
                $(this).text(nameOrigin);
            }
        });

        // matched_viewpointsの表示切替
        $('.matched-vp-area #controlledUL').each(function () {
            var totalLen = 0;
            var maxLen = 30;
            var shown = [];
            var hidden = false;
            var $lis = $(this).find('li');
            $lis.each(function (idx) {
                if (!$(this).data('origin')) {
                    $(this).attr('data-origin', $(this).text());
                }
                // 毎回元テキストに戻す
                var txt = $(this).data('origin');
                $(this).text(txt);
                $(this).show();

                var len = 0;
                for (var i = 0; i < txt.length; i++) {
                    len += (txt.charCodeAt(i) > 255) ? 1 : 0.5;
                }
                if (!hidden && totalLen + len <= maxLen) {
                    totalLen += len;
                    shown.push(this);
                } else {
                    $(this).hide();
                    hidden = true;
                }
            });
            // 末尾に...を追加
            if (hidden && shown.length > 0) {
                var $lastLi = $(shown[shown.length - 1]);
                var originTxt = $lastLi.data('origin');
                $lastLi.text(originTxt + '...');
            }
        });
    }

    // 初回実行
    updateDisplay();

    // ウィンドウリサイズ時に再実行
    $(window).resize(function () {
        updateDisplay();
    });

    // index-panel-itemクリック時のスクロール位置保存
    $('.index-panel-item').on('click', function () {
        const scrollPosition = $('.index-panel').scrollTop();
        sessionStorage.setItem('indexPanelScroll', scrollPosition);
    });
    // index-panelのスクロール位置を復元
    const savedScroll = sessionStorage.getItem('indexPanelScroll');
    if (savedScroll !== null) {
        $('.index-panel').scrollTop(savedScroll || 0);
        // セッションストレージのスクロール位置をクリア
        sessionStorage.removeItem('indexPanelScroll');
    }

    function countChars(strOrigin, strLength) {
        var strInfo = { "is_long": false, "max_idx": 0 };
        var cnt = 0;
        for (var i = 0; i < strOrigin.length; i++) {
            // 全角文字は1、半角文字は0.5としてカウント
            cnt += (strOrigin.charCodeAt(i) > 255) ? 1 : 0.5;
            if (cnt >= strLength) {
                strInfo["is_long"] = true;
                strInfo["max_idx"] = i;
                break;
            }
        }
        return strInfo;
    }
});