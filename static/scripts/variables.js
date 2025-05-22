'use strict';

const thumb_list = game_info['thumbnails'];
const video_list = game_info['videos_max'];
const screenshot_list = game_info['screenshots'];
screenshot_list.forEach(function(path) {
    thumb_list.push(path);
});
const about_the_game = game_info['about_the_game'];
$('.description').html(about_the_game);