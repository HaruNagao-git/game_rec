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

            if (name_origin.length >= nameLength) {
                $(this).text(`${name_origin.substring(0, nameLength)}...`);
            }
            else {
                $(this).text(name_origin);
            }
        });

        $('.text-area-desc').each(function() {
            var desc_origin = $(this).data('desc');
            
            if (desc_origin.length >= descLength) {
                $(this).text(`${desc_origin.substring(0, nameLength)}...`);
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