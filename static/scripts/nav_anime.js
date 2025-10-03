'use strict';

const $btn = $('.btn-menu');
const $nav = $('.main-nav');
$btn.on('click', () => {
	$nav.toggleClass('open-menu');
	if ($btn.text() == 'Menu') {
		$btn.text('Close');
	} else {
		$btn.text('Menu');
	}
});