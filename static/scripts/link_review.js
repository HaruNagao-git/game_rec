'use strict';

// review-infoのレビュー内でevaluationに一致する部分をリンク化する
$(function () {
    const reviewExp = gameInfo["review_exp"] || {};
    if (Object.keys(reviewExp).length === 0) {
        return;
    }
    $('.review-panel').each(function () {
        const $panel = $(this);
        const reviewId = $panel.data('review-id');
        const reviewObj = reviewExp[reviewId];
        const vpList = reviewObj['vp_list'];
        let reviewText = reviewObj['text'];

        // 空白を無視してマッチするための処理
        vpList.forEach(function (vp, idx) {
            if (vp.evaluation && vp.eval_sentence) {
                // 評価文とレビュー文の空白・改行を除去した比較用文字列を作成
                const evaluation = vp.evaluation.replace(/『/g, '「').replace(/』/g, '」');
                console.log('評価:', evaluation);
                const evalNoSpace = evaluation.replace(/[\s\n]/g, '');
                const textNoSpace = reviewText.replace(/[\s\n]/g, '');

                // textNoSpace内で評価文が現れる位置を探す
                const matchIdx = textNoSpace.indexOf(evalNoSpace);
                if (matchIdx === -1) return; // 見つからなければスキップ

                // 元のreviewTextで、空白・改行を無視して一致する部分のインデックスを特定
                let origStart = -1, origEnd = -1, evalCount = 0;
                for (let i = 0, j = 0; i < reviewText.length && evalCount < evalNoSpace.length; i++) {
                    if (!/[\s\n]/.test(reviewText[i])) {
                        if (evalCount === 0 && j === matchIdx) origStart = i;
                        if (j >= matchIdx && evalCount < evalNoSpace.length) {
                            evalCount++;
                            if (evalCount === evalNoSpace.length) origEnd = i + 1;
                        }
                        j++;
                    }
                }
                if (origStart !== -1 && origEnd !== -1) {
                    // マッチ部分をリンク化
                    const matchedStr = reviewText.slice(origStart, origEnd);
                    const link = `<a href="#" class="evaluation-link" data-idx="${idx}" data-review-id="${reviewId}">${matchedStr}</a>`;
                    reviewText = reviewText.slice(0, origStart) + link + reviewText.slice(origEnd);
                }
            }
        });
        // 最後に\n→<br>変換
        reviewText = reviewText.replace(/\n/g, '<br>');
        $panel.find('.review-text p').html(reviewText);
    });

    // リンククリック時にvp-infoへ表示
    $('.review-panel').on('click', '.evaluation-link', function (e) {
        e.preventDefault();
        const idx = $(this).data('idx');
        const reviewId = $(this).data('review-id');
        const vp = gameInfo['review_exp'][reviewId]['vp_list'][idx];

        const $panel = $(this).closest('.review-panel');
        // .sim-group spanのクラスをリセットしてから追加
        $panel.find('.sim-group span').removeClass(function (index, className) {
            return (className.match(/(^|\s)main-group-\S+/g) || []).join(' ');
        });
        $panel.find('.sim-group span').addClass(`main-group-${vp.main_group}`).text(vp.sim_group || '');
        $panel.find('.vp-name span').text(vp.viewpoint || '');
        $panel.find('.eval-sentence span').text(vp.eval_sentence || '');
    });
});