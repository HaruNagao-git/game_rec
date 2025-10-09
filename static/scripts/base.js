'use strict';

window.currentVideoIndex = 0;
window.currentQuality = '480p'; // 初期画質
const $player = $('.custom-video-player');
const $playPauseBtn = $('#playPauseBtn');
const $mediaLoading = $('#mediaLoading');
const $video = $('#mainVideo');

// ボタンのフォントアイコン(Font Awesome)
const playBtnFont = $('<i>', { class: 'fa-solid fa-play' });
const pauseBtnFont = $('<i>', { class: 'fa-solid fa-pause' });

$(function () {
    // 再生・一時停止
    $playPauseBtn.on('click', function () {
        if ($video[0].paused) {
            $video[0].play();
            $playPauseBtn.html(pauseBtnFont).attr("title", "一時停止 (k)");
        } else {
            $video[0].pause();
            $playPauseBtn.html(playBtnFont).attr("title", "再生 (k)");
        }
    });

    $video.on('ended', function () {
        $playPauseBtn.html(playBtnFont); // 動画終了時に再生アイコンに戻す
    });

    // マウスホバーでコントロール表示/非表示
    let hideTimeout;
    $player.on('mousemove', function () {
        if (!$video[0].paused) {
            $player.removeClass('hide-controls');
            clearTimeout(hideTimeout);
            hideTimeout = setTimeout(() => {
                $player.addClass('hide-controls');
            }, 5000);
        } else {
            $player.removeClass('hide-controls');
        }
    });

    // 初期状態は表示
    $player.removeClass('hide-controls');

    $video.on('play', function () {
        // 再生中はホバーで隠す
    });
    $video.on('pause', function () {
        // 一時停止中は常に表示
        $player.removeClass('hide-controls');
    });
});


// キーボード入力で動画プレイヤーを操作
$(function () {
    $(document).on('keydown', function (e) {
        // 入力欄やテキストエリアにフォーカス中は無効化
        if ($(e.target).is('input,textarea')) return;

        switch (e.key.toLowerCase()) {
            case 'k': // 再生・一時停止
                if ($video[0].paused) {
                    $video[0].play();
                    $playPauseBtn.html(pauseBtnFont).attr("title", "一時停止 (k)");
                }
                else {
                    $video[0].pause();
                    $playPauseBtn.html(playBtnFont).attr("title", "再生 (k)");
                }
                e.preventDefault();
                break;
            case 'f': // 全画面切替
                if (!document.fullscreenElement) {
                    $player[0].requestFullscreen();
                }
                else {
                    document.exitFullscreen();
                }
                e.preventDefault();
                break;
            case 'm': // ミュート/ミュート解除
                if ($video[0].volume > 0) {
                    $video[0].volume = 0;
                }
                else {
                    $video[0].volume = 1;
                }
                //アイコン更新
                if ($video[0].volume == 0) {
                    $('#volumeIconSymbol').html($('<i>', { class: 'fa-solid fa-volume-xmark' }));
                }
                else {
                    $('#volumeIconSymbol').html($('<i>', { class: 'fa-solid fa-volume-high' }));
                }
                const percent = $video[0].volume * 100; // 0〜100
                const $volumeBar = $('#volumeBar');
                $volumeBar.css('--vol-progress', percent + '%');
                e.preventDefault();
                break;
            case 'arrowleft':
            case 'j': // 10秒戻る
                $video[0].currentTime = Math.max(0, $video[0].currentTime - 10);
                e.preventDefault();
                break;
            case 'arrowright':
            case 'l': // 10秒進める
                $video[0].currentTime = Math.min($video[0].duration, $video[0].currentTime + 10);
                e.preventDefault();
                break;
        }
    });
});