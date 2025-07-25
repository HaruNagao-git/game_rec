'use strict';

document.addEventListener('DOMContentLoaded', function() {
    // チェックボックスをすべて取得
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const choosedDiv = document.querySelector('.aspect-area-choosed');

    function updateChoosed() {
        // 選択されたラベルを取得
        const checkedLabels = [];
        checkboxes.forEach(cb => {
            if (cb.checked) {
                // ラベル要素内のspanのテキストを取得
                const label = cb.closest('label').querySelector('span');
                if (label) {
                    checkedLabels.push(label.textContent.trim());
                }
            }
        });
        // 表示を更新
        choosedDiv.innerHTML = checkedLabels.length > 0
            ? checkedLabels.map(l => `<li>${l}</li>`).join(' ')
            : '<li class="text-muted">未選択</li>';
    }

    // 初期表示
    updateChoosed();

    // チェックボックスの変更時に更新
    checkboxes.forEach(cb => {
        cb.addEventListener('change', updateChoosed);
    });
});