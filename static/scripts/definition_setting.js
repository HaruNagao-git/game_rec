'use strict';

$(function () {
    const $settingsBtn = $('#settingsBtn');
    const $qualityMenu = $('#qualityMenu');

    const videoData = gameInfo['videos'] || {};

    if (Object.keys(videoData).length === 0) {
        // 動画データがない場合は設定メニューを非表示にする
        $settingsBtn.hide();
        return;
    }
    // 歯車メニューで画質メニュー表示
    $settingsBtn.on('click', function (e) {
        e.stopPropagation();
        $qualityMenu.toggle();
    });
    $(document).on('click', function () {
        $qualityMenu.hide();
    });

    // 画質選択
    $qualityMenu.find('li').on('click', function () {
        $mediaLoading.show(); // ローディング表示
        // 選択状態を更新
        $qualityMenu.find('li').removeClass('selected');
        $(this).addClass('selected');

        // 動画インデックスと画質を取得
        const quality = $(this).data('quality');
        const newSrc = videoData[currentVideoIndex][quality];

        // 再生位置・状態を保存
        const currentTime = $video[0].currentTime;
        const wasPaused = $video[0].paused;

        // 一時的にイベントを設定
        $video.one('loadedmetadata', function () {
            $video[0].currentTime = currentTime;
            if (!wasPaused) {
                $video[0].play();
                $playPauseBtn.html(pauseBtnFont).attr("title", "一時停止");
            } else {
                $playPauseBtn.html(playBtnFont).attr("title", "再生");
            }
        });

        // 画質変更後のロード完了時にローディング非表示
        $video.one('loadeddata', function () {
            $mediaLoading.hide();
        });

        // 切り替え
        $video.attr('src', newSrc);

        // 状態を保存
        currentQuality = quality;
        $qualityMenu.hide();
    });
});