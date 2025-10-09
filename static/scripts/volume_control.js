'use strict';

$(function () {
    const $volumeBar = $('#volumeBar');
    const $volumeIcon = $('#volumeIcon');
    const $volumeIconSymbol = $('#volumeIconSymbol');

    // ボタンのフォントアイコン(Font Awesome)
    const volumeBtnFont = $('<i>', { class: 'fa-solid fa-volume-high' });
    const muteBtnFont = $('<i>', { class: 'fa-solid fa-volume-xmark' });

    // 音量変更時に呼び出し
    $volumeBar.on('input', updateVolumeMeter);
    $volumeBar.on('volumechange', updateVolumeMeter);
    updateVolumeMeter();

    // ボリュームアイコンのフォントサイズを設定
    $volumeIconSymbol.find('i').css('font-size', '1rem');

    // 音量変更時アイコン切替
    $volumeBar.on('input', function () {
        $video[0].volume = $volumeBar.val();
        updateVolumeIcon($video[0].volume);
    });
    $video.on('volumechange', function () {
        $volumeBar.val($video[0].volume);
        updateVolumeIcon($video[0].volume);
    });

    // アイコンをクリックでミュート/解除
    $volumeIcon.on('click', function () {
        if ($video[0].volume > 0) {
            $video[0].volume = 0;
        } else {
            $video[0].volume = 1;
        }
        updateVolumeIcon($video[0].volume);
        const percent = $video[0].volume * 100; // 0〜100
        $volumeBar.css('--vol-progress', percent + '%');
    });
    // ボリュームバーの非表示遅延
    let volumeHideTimeout = null;
    $('.volume-control').on('mouseenter', function () {
        clearTimeout(volumeHideTimeout);
        $(this).find('.volume-bar').stop(true, true).fadeIn(100).addClass('show');

    });

    // 2秒後に.volume-barのshowを削除して非表示
    $('.volume-control').on('mouseleave', function () {
        const $bar = $(this).find('.volume-bar');
        volumeHideTimeout = setTimeout(function () {
            $bar.fadeOut(300).removeClass('show');
        }, 2000);
    });

    function updateVolumeMeter() {
        const percent = $video[0].volume * 100; // 0〜100
        $volumeBar.css('--vol-progress', percent + '%');
    }
    // 初期スピーカーアイコン
    function updateVolumeIcon(vol) {
        if (vol == 0) {
            $volumeIconSymbol.html(muteBtnFont); // スピーカー斜線
        } else {
            $volumeIconSymbol.html(volumeBtnFont); // 通常スピーカー
        }
    }
})