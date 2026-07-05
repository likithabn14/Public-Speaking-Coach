let mediaRecorder;
let audioChunks = [];

let startBtn = document.getElementById("startBtn");
let stopBtn = document.getElementById("stopBtn");
let timer = document.getElementById("timer");
let status = document.getElementById("status");

let seconds = 0;
let interval;

startBtn.addEventListener("click", async () => {

    const stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    });

    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];

    mediaRecorder.start();

    status.innerHTML = "🎤 Recording...";

    startBtn.disabled = true;
    stopBtn.disabled = false;

    seconds = 0;

    interval = setInterval(() => {

        seconds++;

        let min = String(Math.floor(seconds / 60)).padStart(2, "0");
        let sec = String(seconds % 60).padStart(2, "0");

        timer.innerHTML = `${min}:${sec}`;

    }, 1000);

    mediaRecorder.ondataavailable = (event) => {

        if (event.data.size > 0) {

            audioChunks.push(event.data);

        }

    };

});


stopBtn.addEventListener("click", () => {

    mediaRecorder.stop();

    clearInterval(interval);

    startBtn.disabled = false;
    stopBtn.disabled = true;

    status.innerHTML = "⏳ Uploading & Analyzing...";

});


mediaRecorderFinished = () => {};

document.addEventListener("DOMContentLoaded", () => {

});


function uploadAudio(blob) {

    const formData = new FormData();

    formData.append("audio", blob, "speech.webm");

    fetch("/analyze", {

        method: "POST",

        body: formData

    })
    .then(response => response.text())
    .then(html => {

        document.open();
        document.write(html);
        document.close();

    })
    .catch(error => {

        alert("Error uploading audio.");

        console.log(error);

    });

}


document.addEventListener("mouseup", () => {

    if (!mediaRecorder) return;

    mediaRecorder.onstop = () => {

        const blob = new Blob(audioChunks, {

            type: "audio/webm"

        });

        uploadAudio(blob);

    };

});
