'use strict';

$(function () {
    const $backwardBtn = $('#backwardBtn');
    const $forwardBtn = $('#forwardBtn');
    const $timeBar = $('#timeBar');
    const $timeIndicator = $('#timeIndicator');
    const $currentTime = $('#currentTime');
    const $duration = $('#duration');

    // 10秒戻す
    $backwardBtn.on('click', function () {
        $mediaLoading.show(); // ローディング表示
        $video[0].currentTime = Math.max(0, $video[0].currentTime - 10);
        $video.one('seeked', function () {
            $mediaLoading.hide(); // シーク完了でローディング非表示
        });
    });
    // 10秒進める
    $forwardBtn.on('click', function () {
        $mediaLoading.show(); // ローディング表示
        $video[0].currentTime = Math.min($video[0].duration, $video[0].currentTime + 10);
        $video.one('seeked', function () {
            $mediaLoading.hide(); // シーク完了でローディング非表示
        });
    });
    // タイムバー更新
    $video.on('timeupdate', function () {
        $timeBar.val(($video[0].currentTime / $video[0].duration) * 100);
        $currentTime.text(formatTime($video[0].currentTime));
    });
    $timeBar.val(0); // ページロード時に左端
    $video.on('loadedmetadata', function () {
        $timeBar.val(0);
        $playPauseBtn.html(playBtnFont).attr("title", "再生");
        $duration.text(formatTime($video[0].duration));
        updateTimeBar();
    });
    // ページロード時にも明示的にdurationをセット（loadedmetadataが既に発火している場合の対策）
    if ($video[0].readyState >= 1) {
        $duration.text(formatTime($video[0].duration));
    }

    // タイムバー操作
    $timeBar.on('input', function () {
        $video[0].currentTime = ($timeBar.val() / 100) * $video[0].duration;
        updateTimeBar();
    });
    // タイムバーにマウスオーバーしたときに時間を表示
    $timeBar.on('mousemove', function (e) {
        const video = $video[0];
        const barOffset = $timeBar.offset();
        const barWidth = $timeBar.width();
        const mouseX = e.pageX - barOffset.left;
        const percent = Math.min(Math.max(mouseX / barWidth, 0), 1);
        const jumpTime = percent * video.duration;

        $timeIndicator.text(formatTime(jumpTime));
        // インジケーターの位置をマウスに合わせて移動
        $timeIndicator.css({
            left: (mouseX) + 'px',
            display: 'block'
        });
    });
    $timeBar.on('mouseleave', function () {
        $timeIndicator.hide();
    });

    $video.on('timeupdate loadedmetadata', updateTimeBar);

    function formatTime(sec) {
        sec = Math.floor(sec);
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    }
    function updateTimeBar() {
        const percent = ($video[0].currentTime / $video[0].duration) * 100;
        $timeBar.val(percent);
        $timeBar.css('--progress', percent + '%');
        $currentTime.text(formatTime($video[0].currentTime));
    }
});