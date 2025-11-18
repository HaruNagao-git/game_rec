'use strict';

$(function () {
    // チェックボックスをすべて取得
    const $checkboxLabels = $('.checkbox-area label');
    const $checkboxes = $('input[type="checkbox"]');
    const $choosedDiv = $('.viewpoint-area-choosed');
    const $jsDetails = $('.js-details');
    const $vpDescText = $('.vp-desc-text');
    const $vpDescIcon = $('#vpDescIcon');
    // アコーディオンにホバーしたときの動作
    if (subgroupDesc) {
        $jsDetails.on('mouseenter', function () {
            const subgroupID = $(this).data('id').toString();
            const subgroupLabel = $(this).data('label').toString();
            console.log('hovered subgroupID:', subgroupID);
            const description = subgroupDesc[subgroupID] || '説明が見つかりません。';
            $vpDescText.text(description);
            $vpDescIcon.text(subgroupLabel);
        });
    }
    // チェックボックスにホバーしたときの動作
    if (simGroupDesc) {
        // チェックボックスにホバーしたときにvp-desc-textを更新
        $checkboxLabels.on('mouseenter', function () {
            const simGroupID = $(this).find('input[type="checkbox"]').val().toString();
            const simGroupLabel = $(this).find('span').text().trim();
            console.log('hovered simGroupID:', simGroupID);
            const description = simGroupDesc[simGroupID] || '説明が見つかりません。';
            $vpDescText.text(description);
            $vpDescIcon.text(simGroupLabel);
        });
    }
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