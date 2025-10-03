'use strict';

// メディアクエリで条件分岐
// 画面幅が768px以上の場合
// namesを55文字まで表示, short_descを130文字まで表示
// 画面幅が768px未満の場合
// namesを30文字まで表示, short_descを60文字まで表示
//jQueryを使用

$(document).ready(function () {
    function updateDisplay() {
        var isWideScreen = $(window).width() >= 768;
        var nameLength = isWideScreen ? 55 : 30;
        var descLength = isWideScreen ? 130 : 60;

        $('.text-area-name').each(function () {
            // 基のテキストをdata属性に保存
            var name_origin = $(this).data('name');

            var name_info = countChars(name_origin, nameLength);
            if (name_info.is_long) {
                $(this).text(`${name_origin.substring(0, name_info.max_idx)}...`);
            }
            else {
                $(this).text(name_origin);
            }
        });

        $('.text-area-desc').each(function () {
            var desc_origin = $(this).data('desc');

            var desc_info = countChars(desc_origin, descLength);
            if (desc_info.is_long) {
                $(this).text(`${desc_origin.substring(0, desc_info.max_idx)}...`);
            }
            else {
                $(this).text(desc_origin);
            }
        });

        // matched_viewpointsの表示切替
        $('.matched-viewpoints-area').each(function () {
            var totalLen = 0;
            var maxLen = isWideScreen ? 50 : 25;
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
});

function countChars(str_origin, str_length) {
    var str_info = { "is_long": false, "max_idx": 0 };
    var cnt = 0;
    for (var i = 0; i < str_origin.length; i++) {
        // 全角文字は1、半角文字は0.5としてカウント
        cnt += (str_origin.charCodeAt(i) > 255) ? 1 : 0.5;
        if (cnt >= str_length) {
            str_info["is_long"] = true;
            str_info["max_idx"] = i;
            break;
        }
    }
    return str_info;
}