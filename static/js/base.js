// const audioPlayer = document.getElementById("audio-player")
// const play_pause_btn =document.getElementById("play-pause")
// const duration =document.getElementById("total-duration")
// const current_time = document.getElementById("current-time")
// const progress_bar = document.getElementById("progress-bar")
// const progress = document.getElementById("progress")

// playButton.addEventListener('click', () => {
//     if (playButton.textContent === "Play") {
//         playSong(mySongUrl);
//         playButton.textContent = "Pause";
//     } else {
//         songControls.pause();
//         playButton.textContent = "Play";
//     }
// });


document.addEventListener('DOMContentLoaded', () => {  // Wait for the DOM to load

    const audioPlayer = document.getElementById('audio-player');
    const playPauseButton = document.getElementById('play-pause');
    const progressBar = document.getElementById('progress-bar');
    const progress = document.getElementById('progress');
    const currentTimeDisplay = document.getElementById('current-time');
    const totalDurationDisplay = document.getElementById('total-duration');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    // ...other controls

    const skipTime = 10; // Seconds to skip

    let isPlaying = false;

    // Load metadata to get duration (important!)
    audioPlayer.addEventListener('loadedmetadata', () => {
        const duration = audioPlayer.duration;
        const formattedDuration = formatTime(duration);
        totalDurationDisplay.textContent = formattedDuration;
    });


    playPauseButton.addEventListener('click', () => {
        if (isPlaying) {
            audioPlayer.pause();
            playPauseButton.innerHTML = '<i class="fa fa-play-circle" aria-hidden="true"></i>'; // Change icon
        } else {
            audioPlayer.play();
            playPauseButton.innerHTML = '<i class="fa fa-pause-circle" aria-hidden="true"></i>'; // Change icon
        }
        isPlaying = !isPlaying;
    });

    audioPlayer.addEventListener('play', () => {
      isPlaying = true; // Ensure isPlaying is correct
      playPauseButton.innerHTML = '<i class="fa fa-pause-circle" aria-hidden="true"></i>';
    });

    audioPlayer.addEventListener('pause', () => {
        isPlaying = false; // Ensure isPlaying is correct
        playPauseButton.innerHTML = '<i class="fa fa-play-circle" aria-hidden="true"></i>';
    });

    audioPlayer.addEventListener('timeupdate', () => {
        updateProgress();
        updateCurrentTime();
    });

    progressBar.addEventListener('click', (event) => {
        const totalWidth = progressBar.offsetWidth;
        const clickX = event.offsetX;
        const newPosition = (clickX / totalWidth) * audioPlayer.duration;
        audioPlayer.currentTime = newPosition;
    });

    function updateProgress() {
        const progressPercentage = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        progress.style.width = `${progressPercentage}%`;
    }

    function updateCurrentTime() {
        const currentTime = audioPlayer.currentTime;
        const formattedTime = formatTime(currentTime);
        currentTimeDisplay.textContent = formattedTime;
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        const paddedSeconds = remainingSeconds < 10 ? '0' + remainingSeconds : remainingSeconds;
        return `${minutes}:${paddedSeconds}`;
    }

    nextButton.addEventListener('click', () => {
        const newTime = audioPlayer.currentTime + skipTime;
        if (newTime <= audioPlayer.duration) {  // Prevent going beyond the end
            audioPlayer.currentTime = newTime;
        } else {
            audioPlayer.currentTime = audioPlayer.duration; // Go to the end if skipping exceeds duration
        }
    });

    prevButton.addEventListener('click', () => {
        const newTime = audioPlayer.currentTime - skipTime;
        if (newTime >= 0) { // Prevent going before the start
            audioPlayer.currentTime = newTime;
        } else {
            audioPlayer.currentTime = 0; // Go to the beginning if skipping goes below 0
        }
    });



});