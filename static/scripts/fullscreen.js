'use strict';

$(function () {
    const $fullscreenBtn = $('#fullscreenBtn');

    // フルスクリーン
    $fullscreenBtn.on('click', function () {
        if (!document.fullscreenElement) {
            $player[0].requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    });
    $(document).on('fullscreenchange', function () {
        setFullscreen(!!document.fullscreenElement);
    });

    // フルスクリーン切替
    function setFullscreen(isFullscreen) {
        if (isFullscreen) {
            $player.addClass('fullscreen');
        } else {
            $player.removeClass('fullscreen');
        }
    }
});