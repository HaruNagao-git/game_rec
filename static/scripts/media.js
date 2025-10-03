'use strict';

thumb_list.forEach(function (thumb_path, index) {
	let $thumb_elm = $('<div>', { class: 'slide' }); // slide要素
	if (index < video_list.length) {
		// video_listの要素にmovieクラスを追加
		$thumb_elm.addClass('movie').append($('<img>', { src: thumb_path, class: 'thumb' }));
	} else {
		$thumb_elm.append($('<img>', { src: thumb_path['338p'], class: 'thumb' }));
	}
	// .slide-areaに要素を追加
	$('.slide-area').append($thumb_elm);

	// クリック時
	$('.slide').eq(index).on('click', function () {
		$mediaLoading.show(); // ローディング表示
		// 現在のスクロール位置を取得
		const scrollPosition = $('window').scrollTop();

		// 全ての.slideから.currentを外す
		$('.slide').removeClass('current');
		// クリックした要素に.currentを追加
		$(this).addClass('current');

		// 要素のインデックスを取得
		let index = $(this).index();
		let thumb_path = thumb_list[index];
		// movieクラスがあれば動画を、それ以外は画像を表示
		if ($(this).hasClass('movie')) {
			currentVideoIndex = index; // 現在の動画インデックスを更新
			if ($('.video').hasClass('hidden')) { // videoにhiddenタグがあった場合
				// videoのhiddenタグを削除し、imageのhiddenタグを追加
				$('.video').toggleClass('hidden');
				$('.image').toggleClass('hidden');
			}

			const $video = $('.video').find('video');
			$video.one('loadeddata', function () {
				$mediaLoading.hide(); // 読み込み完了でローディング非表示
			});
			$video.attr('src', video_list[index][currentQuality]); // videoタグのsrcを変更
			$video.attr('poster', thumb_path); // videoタグのposterを変更
		} else {
			if ($('.image').hasClass('hidden')) { // imgにhiddenタグがあった場合
				// imageのhiddenタグを削除し、videoのhiddenタグを追加＆再生をストップ
				$('.video').toggleClass('hidden').find('video').get(0).pause();
				$('.image').toggleClass('hidden');
			}

			const $img = $('.image').find('img');
			$img.on('load', function () {
				$mediaLoading.hide(); // 読み込み完了でローディング非表示
			});
			$img.attr('src', thumb_path['1080p']); // imgタグのposterを変更
		}
		// スクロール位置を調整
		$('window').scrollTop(scrollPosition);
	});
});

// .slide-areaの幅を調整
const slide_width = 116;
const slide_gap = parseInt($('.slide-area').css('gap'));
const slide_padding = parseInt($('.slide-area').css('padding'));
const slide_area_width = thumb_list.length * (slide_width + slide_gap) - slide_gap + slide_padding * 2;
$('.slide-area').css('width', `${slide_area_width}px`);

// 最初の.slideに.currentを追加
$('.slide').first().addClass('current');

// 動画のプリロード
for (let i = 0; i < video_list.length; i++) {
	preloadVideo(video_list[i], thumb_list[i]);
}
// 画像のプリロード
for (let i = video_list.length; i < thumb_list.length; i++) {
	preloadImage(thumb_list[i]);
}
function preloadVideo(video_path, thumb_path) {
	let videoSDTag = $('<video>').attr({ 'src': video_path['480p'], 'poster': thumb_path, 'controls': true });
	let videoHDTag = $('<video>').attr({ 'src': video_path['1080p'], 'poster': thumb_path, 'controls': true });
}
function preloadImage(image_path) {
	let img338pTag = $('<img>').attr('src', image_path['338p']);
	let img1080pTag = $('<img>').attr('src', image_path['1080p']);
}