'use strict';

const thumb_list = game_info['thumbnails'];
const video_list = game_info['videos'];
const screenshot_list = game_info['screenshots'];
const review_exp = game_info['review_exp'];
const screenshot1080p_list = [];
screenshot_list.forEach(obj => {
    screenshot1080p_list.push(obj['1080p']);
});
screenshot_list.forEach(function (path) {
    thumb_list.push(path);
});
const about_the_game = game_info['about_the_game'];
$('.description').html(about_the_game);