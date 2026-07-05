import whisper
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_silence
import tempfile

FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "actually",
    "basically",
    "literally",
    "you know",
    "so"
]


def analyze_audio(filepath):

    audio = AudioSegment.from_file(filepath)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

    wav_path = temp.name

    temp.close()

    audio.export(wav_path, format="wav")

    recognizer = sr.Recognizer()

    transcript = ""

    try:

        with sr.AudioFile(wav_path) as source:

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio_data = recognizer.record(source)

            transcript = recognizer.recognize_google(audio_data)

    except Exception:

        transcript = "Speech could not be recognized."

    duration = round(len(audio) / 1000, 2)

    words = transcript.split()

    if duration > 0:
        wpm = round((len(words) / duration) * 60)
    else:
        wpm = 0

    silence = detect_silence(
        audio,
        min_silence_len=700,
        silence_thresh=audio.dBFS - 16
    )

    pauses = len(silence)

    fillers = {}

    total_fillers = 0

    lower = transcript.lower()

    for word in FILLER_WORDS:

        count = lower.count(word)

        if count > 0:
            fillers[word] = count

        total_fillers += count

    confidence = 100

    if wpm < 110:
        confidence -= 10

    if wpm > 170:
        confidence -= 10

    confidence -= pauses * 2

    confidence -= total_fillers * 3

    confidence = max(0, min(confidence, 100))

    feedback = []

    if wpm < 110:
        feedback.append("Speak a little faster.")
    elif wpm > 170:
        feedback.append("Try speaking slower.")
    else:
        feedback.append("Excellent speaking speed.")

    if total_fillers > 5:
        feedback.append("Reduce filler words.")

    else:
        feedback.append("Good control over filler words.")

    if pauses > 10:
        feedback.append("Avoid unnecessary pauses.")

    else:
        feedback.append("Good pause control.")

    if confidence >= 90:
        feedback.append("Excellent confidence!")

    elif confidence >= 75:
        feedback.append("Good confidence.")

    else:
        feedback.append("Practice speaking every day.")

    return {
        "transcript": transcript,
        "duration": duration,
        "wpm": wpm,
        "pauses": pauses,
        "fillers": fillers,
        "confidence": confidence,
        "feedback": feedback
    }