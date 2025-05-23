'use strict';

// モーダルウィンドウの前後移動用変数
let currentImageIndex = -1;
// thumb_listの最初の画像index
const firstImageIndex = video_list.length;
// screenshot部分の長さ
const screenshotLength = thumb_list.length - firstImageIndex;

// モーダルを表示する関数
function showModal(index) {
	currentImageIndex = index - firstImageIndex;
	const src = thumb_list[index];

	// モーダルの画像を更新
	pageNum();
	$('#modalImage').attr('src', src);
	const modal = new bootstrap.Modal($('#screenshotModal'));
	modal.show();
}

// 前後ボタンのクリックイベント
$('#prevButton').on('click', function() {
	if (currentImageIndex > 0) {
		currentImageIndex--;
	} else {
		currentImageIndex = screenshotLength - 1;
	}

	pageNum();
	$('#modalImage').attr('src', thumb_list[currentImageIndex + firstImageIndex]);
});
$('#nextButton').on('click', function() {
	if (currentImageIndex < screenshotLength - 1) {
		currentImageIndex++;
	} else {
		currentImageIndex = 0;
	}

	pageNum();
	$('#modalImage').attr('src', thumb_list[currentImageIndex + firstImageIndex]);
});
// 何枚目の画像かを表示
function pageNum() {
	$('.page-num').text(`${currentImageIndex+1}/${screenshotLength}`);
}

// .imageをクリックしたときの処理
$('.media-main .image img').on('click', function() {
	const parent = $(this).closest('.image');
	if (!parent.hasClass('.movie')) {
		const index = thumb_list.indexOf($(this).attr('src'));
		if (index !== -1) {
			showModal(index);
		}
	}
});
// モーダルウィンドウを閉じたときの処理
$('#screenshotModal').on('hidden.bs.modal', function() {
	// モーダルを閉じたときに画像をリセット
	currentImageIndex = -1;
	$('#modalImage').attr('src', '');
	$('.page-num').text('');
	// フォーカスを外す
	document.activeElement.blur();
});