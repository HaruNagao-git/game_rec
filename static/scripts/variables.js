'use strict';

let thumbList = gameInfo['thumbnails'];
const videoList = gameInfo['videos'];
const screenshotList = gameInfo['screenshots'];
let screenshot1080pList = [];
screenshotList.forEach(obj => {
    screenshot1080pList.push(obj['1080p']);
});
screenshotList.forEach(function (path) {
    thumbList.push(path);
});
const aboutTheGame = gameInfo['about_the_game'];
$('.description').html(aboutTheGame);