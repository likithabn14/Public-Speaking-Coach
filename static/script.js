const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const analyzeBtn = document.getElementById("analyzeBtn");

const transcriptBox = document.getElementById("transcript");

const hiddenTranscript = document.getElementById("hiddenTranscript");
const hiddenDuration = document.getElementById("hiddenDuration");

const timer = document.getElementById("timer");
const status = document.getElementById("status");

let recognition;
let finalTranscript = "";
let seconds = 0;
let interval;

if (!SpeechRecognition) {

    status.innerHTML = "❌ Speech Recognition is not supported in this browser.";

    startBtn.disabled = true;

} else {

    recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {

        status.innerHTML = "🎤 Listening...";

    };

    recognition.onresult = (event) => {

        let interimTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {

            const text = event.results[i][0].transcript;

            if (event.results[i].isFinal) {

                finalTranscript += text + " ";

            } else {

                interimTranscript += text;

            }

        }

        transcriptBox.value = finalTranscript + interimTranscript;

    };

    recognition.onerror = (event) => {

        console.log(event.error);

        status.innerHTML = "❌ " + event.error;

        clearInterval(interval);

        startBtn.disabled = false;
        stopBtn.disabled = true;

    };

    recognition.onend = () => {

        clearInterval(interval);

        startBtn.disabled = false;
        stopBtn.disabled = true;

        status.innerHTML = "✅ Speech captured.";

        if (finalTranscript.trim() !== "") {

            hiddenTranscript.value = finalTranscript.trim();

            hiddenDuration.value = seconds;

            document.getElementById("speechForm").submit();

        }

    };

}

startBtn.onclick = () => {

    if (!recognition) return;

    finalTranscript = "";

    transcriptBox.value = "";

    seconds = 0;

    timer.innerHTML = "00:00";

    recognition.start();

    startBtn.disabled = true;
    stopBtn.disabled = false;

    interval = setInterval(() => {

        seconds++;

        let min = String(Math.floor(seconds / 60)).padStart(2, "0");
        let sec = String(seconds % 60).padStart(2, "0");

        timer.innerHTML = `${min}:${sec}`;

    }, 1000);

};

stopBtn.onclick = () => {

    if (!recognition) return;

    recognition.stop();

};

analyzeBtn.onclick = () => {

    const text = transcriptBox.value.trim();

    if (text === "") {

        alert("Please speak or type your speech first.");

        return;

    }

    hiddenTranscript.value = text;

    hiddenDuration.value = seconds;

    document.getElementById("speechForm").submit();

};
