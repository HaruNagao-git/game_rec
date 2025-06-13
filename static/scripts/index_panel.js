// メディアクエリで条件分岐
// 画面幅が600px以上の場合
// namesを50文字まで表示, short_descを100文字まで表示
// 画面幅が600px未満の場合
// namesを20文字まで表示, short_descを50文字まで表示
//jQueryを使用

$(document).ready(function() {
    function updateDisplay() {
        var isWideScreen = $(window).width() >= 600;
        var nameLength = isWideScreen ? 50 : 30;
        var descLength = isWideScreen ? 200 : 60;

        $('.text-area-name').each(function() {
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

        $('.text-area-desc').each(function() {
            var desc_origin = $(this).data('desc');
            
            var desc_info = countChars(desc_origin, descLength);
            if (desc_info.is_long) {
                $(this).text(`${desc_origin.substring(0, desc_info.max_idx)}...`);
            }
            else {
                $(this).text(desc_origin);
            }
        });
    }

    // 初回実行
    updateDisplay();

    // ウィンドウリサイズ時に再実行
    $(window).resize(function() {
        updateDisplay();
    });
});

function countChars(str_origin, str_length) {
    var str_info = {"is_long": false, "max_idx": 0};
    var cnt=0;
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