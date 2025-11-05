'use strict';

// デスクトップ時とモバイル時で、ログイン画面の背景画像を変更
$(document).ready(function () {
    function updateDisplay() {
        var isWideScreen = $(window).width() >= 768;
        var imgPath = isWideScreen ? desktopImgPath : mobileImgPath;

        // 背景画像の更新
        $('.background-img').attr('src', imgPath);
    };

    // 初回実行
    updateDisplay();

    // ウィンドウリサイズ時に再実行
    $(window).resize(function () {
        updateDisplay();
    });
});