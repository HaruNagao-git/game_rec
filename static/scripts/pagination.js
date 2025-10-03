'use strict';

const Pagination = () => {
    const $container = $('.pagination');
    if (!$container) return;
    const $items = $container.find('.pagination__items li');
    const $prevLink = $container.find('.pagination__prev');
    const $nextLink = $container.find('.pagination__next');

    // ページ番号クリックでリンク遷移
    $items.find('a').on('click', function(event) {
        // 通常のリンク遷移に任せる（サーバーサイドでページ切り替え）
    });

    // 前へ・次へボタンでリンク遷移
    $prevLink.on('click', function(event) {
        if ($prevLink.hasClass('disabled')) {
            event.preventDefault();
            return;
        }
        window.location.href = $(this).attr('href');
    });
    $nextLink.on('click', function(event) {
        if ($nextLink.hasClass('disabled')) {
            event.preventDefault();
            return;
        }
        window.location.href = $(this).attr('href');
    });
};

$(Pagination);