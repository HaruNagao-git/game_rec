'use strict';

$(document).ready(function () {
    let accordionDetails = '.js-details';
    let accordionSummary = '.js-details-summary';
    let accordionContent = '.js-details-content';
    let speed = 500;

    $(accordionSummary).each(function () {
        $(this).on("click", function (event) {
            // summaryにis-activeクラスを切り替え
            $(this).toggleClass("is-active");
            // デフォルトの挙動を無効化
            event.preventDefault();
            if ($(this).parent($(accordionDetails)).attr("open")) {
                // アコーディオンを閉じるときの処理
                $(this).nextAll($(accordionContent)).slideUp(speed, function () {
                    // アニメーションの完了後にopen属性を取り除く
                    $(this).parent($(accordionDetails)).removeAttr("open");
                    // display:none;を消して、ページ内検索にヒットするようにする
                    $(this).show();
                });
            } else {
                // アコーディオンを開くときの処理
                // open属性を付ける
                $(this).parent($(accordionDetails)).attr("open", "true");
                // いったんdisplay:none;してからslideDownで開く
                $(this).nextAll($(accordionContent)).hide().slideDown(speed);
            }
        });

        $(this).closest(accordionDetails).find('.close-btn').on('click', function (eventclosee) {
            eventclosee.preventDefault();
            //「閉じる」ボタンがクリックされた場合にsummaryの.is-activeを外す
            $(this).closest(accordionDetails).find(accordionSummary).removeClass("is-active");
            //「閉じる」ボタンがクリックされた場合にdetails-contentを閉じる
            $(this).closest(accordionContent).slideUp(speed, function () {
                //「閉じる」ボタンがクリックされた場合にdetailsのopen属性を外す
                $(this).closest(accordionDetails).removeAttr("open");
            });
        });
    });
});