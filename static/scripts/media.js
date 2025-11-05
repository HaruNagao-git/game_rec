'use strict';

$(function () {
	const slideWidth = 116;
	const slideGap = parseInt($('.slide-area').css('gap'));
	const slidePadding = parseInt($('.slide-area').css('padding'));
	const slideAreaWidth = thumbList.length * (slideWidth + slideGap) - slideGap;
	const mediaWindowSize = $('.media-main').width();

	thumbList.forEach(function (thumbPath, index) {
		// 動画のプリロード
		for (let i = 0; i < videoList.length; i++) {
			preloadVideo(videoList[i], thumbList[i]);
		}
		// 画像のプリロード
		for (let i = videoList.length; i < thumbList.length; i++) {
			preloadImage(thumbList[i]);
		}

		let $thumbElm = $('<div>', { class: 'slide' }); // slide要素
		if (index < videoList.length) {
			// videoListの要素にmovieクラスを追加
			$thumbElm.addClass('movie').append($('<img>', { src: thumbPath, class: 'thumb' }));
		} else {
			$thumbElm.append($('<img>', { src: thumbPath['338p'], class: 'thumb' }));
		}
		// .slide-areaに要素を追加
		$('.slide-area').append($thumbElm);

		// クリック時
		$('.slide').eq(index).on('click', function () {
			$mediaLoading.show(); // ローディング表示
			// 現在のスクロール位置を取得
			const scrollPosition = $('window').scrollTop();
			// currentを変更
			changeCurrentSlide($(this), mediaWindowSize, slideWidth);
			// スクロール位置を調整
			$('window').scrollTop(scrollPosition);
		});
	});

	// .slide-areaの幅を調整
	$('.slide-area').width(`${slideAreaWidth}px`);

	// 最初の.slideに.currentを追加
	$('.slide').first().addClass('current');
})

function preloadVideo(videoPath, thumbPath) {
	let videoSDTag = $('<video>').attr({ 'src': videoPath['480p'], 'poster': thumbPath, 'controls': true });
	let videoHDTag = $('<video>').attr({ 'src': videoPath['1080p'], 'poster': thumbPath, 'controls': true });
}
function preloadImage(imagePath) {
	let img338pTag = $('<img>').attr('src', imagePath['338p']);
	let img1080pTag = $('<img>').attr('src', imagePath['1080p']);
}

function changeCurrentSlide($nextSlide, mediaWindowSize, slideWidth) {
	// 全ての.slideから.currentを外す
	$('.slide').removeClass('current');
	// クリックした要素に.currentを追加
	$nextSlide.addClass('current');

	// 要素のインデックスを取得
	let index = $nextSlide.index();
	let thumbPath = thumbList[index];
	// movieクラスがあれば動画を、それ以外は画像を表示
	if ($nextSlide.hasClass('movie')) {
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
		$video.attr('src', videoList[index][currentQuality]); // videoタグのsrcを変更
		$video.attr('poster', thumbPath); // videoタグのposterを変更
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
		$img.attr('src', thumbPath['1080p']); // imgタグのposterを変更
	}

	const $slideArea = $nextSlide.parent();
	const slideAreaScroll = $slideArea.scrollLeft();
	const currentLeft = $nextSlide.position().left; // .currentの左端の位置
	const currentRight = currentLeft + slideWidth; // .currentの右端の位置
	// 右端が見切れていたら右にスクロール
	if (currentRight > mediaWindowSize) {
		$slideArea.animate({ scrollLeft: slideAreaScroll + (currentRight - mediaWindowSize) }, 500);
	}
	// 左端が見切れていたら左にスクロール
	else if (currentLeft < 0) {
		$slideArea.animate({ scrollLeft: slideAreaScroll + currentLeft }, 500);
	}
}