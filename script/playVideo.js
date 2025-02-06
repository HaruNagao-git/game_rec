function playVideo(videoid, appid) {
    fetch("{{url_for('game.get_video')}}",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'videoid': parseInt(videoid),
            'appid': parseInt(appid)
        })
    })
    .then(response => response.json())
    .then(data => {
        const videoElement = document.getElementById('movie');
        videoElement.src = data.video_max;
        videoElement.poster = data.thumbnail;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}