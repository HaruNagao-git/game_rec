'use strtict';

thumb_list.forEach(function(thumb_path, index) {
	let thumb_elm = '';
	if (index < video_list.length) {
		// video_listの要素にmovieクラスを追加
		thumb_elm = `
        <div class="slide movie"><img src=${thumb_path} class="thumb"></img></div>`;
	} else {
		thumb_elm = `
        <div class="slide"><img src=${thumb_path} class="thumb"></img></div>`;
	}
	// .slide-areaに要素を追加
	$('.slide-area').append(thumb_elm);

	// クリック時
	$('.slide').eq(index).on('click', function() {
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
			if ($('.video').hasClass('hidden')) { // videoにhiddenタグがあった場合
				// videoのhiddenタグを削除し、imgのhiddenタグを追加
				$('.video').toggleClass('hidden');
				$('.image').toggleClass('hidden');
			}

			let video_path = video_list[index];
			// videoタグのsrcを変更
			$('.video').find('video').attr('src', video_path);
			// videoタグのposterを変更
			$('.video').find('video').attr('poster', thumb_path);
		} else {
			if ($('.image').hasClass('hidden')) { // imgにhiddenタグがあった場合
				// videoのhiddenタグを削除し、imgのhiddenタグを追加
				$('.video').toggleClass('hidden');
				$('.image').toggleClass('hidden');
			}

			// imgタグのposterを変更
			$('.image').find('img').attr('src', thumb_path);
		}
		// スクロール位置を調整
		$('window').scrollTop(scrollPosition);
	});
});

// .slide-areaの幅を調整
const slide_width=116;
const slide_gap=4;
const slide_padding=3;
const slide_area_width=thumb_list.length*(slide_width+slide_gap)-slide_gap+slide_padding*2;
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
	let videoTag = document.createElement('video');
	videoTag.controls = true;
	videoTag.src = video_path;
	videoTag.poster = thumb_path;
}
function preloadImage(image_path) {
	let imgTag = document.createElement('img');
	imgTag.src = image_path;
}