'use strict';

$(function () {
    // チェックボックスをすべて取得
    const $checkboxes = $('input[type="checkbox"]');
    const $choosedDiv = $('.viewpoint-area-choosed');

    function updateChoosed() {
        // 選択されたラベルを取得
        const checkedLabels = $checkboxes.filter(':checked').map(function () {
            return $(this).closest('label').find('span').text().trim();
        }).get();

        // 表示を更新
        if (checkedLabels.length > 0) {
            $choosedDiv.html(checkedLabels.map(l => `<li>${l}</li>`).join(' '));
        } else {
            $choosedDiv.html('<li class="text-muted">未選択</li>');
        }
    }

    // 初期表示
    updateChoosed();

    // チェックボックスの変更時に更新
    $checkboxes.on('change', updateChoosed);
});