'use strict'
// 初期化
let itemWidth = getItemWidth();

$(window).on('resize', function () {
    // ウィンドウのリサイズ時にスクロール量を再計算
    itemWidth = getItemWidth();
});

$(function () {
    // console.log(itemWidth);
    $('.scroll-btn.left').on('click', function () {
        const $carouselSiblings = $(this).siblings('.checkbox-group-corousel');
        $carouselSiblings.animate({ scrollLeft: $carouselSiblings.scrollLeft() - itemWidth }, 500);
    });
    $('.scroll-btn.right').on('click', function () {
        const $carouselSiblings = $(this).siblings('.checkbox-group-corousel');
        $carouselSiblings.animate({ scrollLeft: $carouselSiblings.scrollLeft() + itemWidth }, 500);
    });
});

function getItemWidth() {
    // carouselの子要素の幅を取得して、スクロール量を調整する
    const $carousel = $('.checkbox-group-corousel');
    const $details = $carousel.find('.details');
    return $details.outerWidth(true) * 3; // 3つ分スクロール
}