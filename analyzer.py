import whisper
from pydub import AudioSegment
from pydub.silence import detect_silence
import tempfile

# Load Whisper model only once
model = whisper.load_model("tiny")

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

    # Read uploaded audio (webm)
    audio = AudioSegment.from_file(filepath)

    # Create temporary wav file
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav_path = temp_wav.name
    temp_wav.close()

    # Export as wav
    audio.export(wav_path, format="wav")

    # Speech to text
    result = model.transcribe(wav_path)

    transcript = result["text"].strip()

    # Duration
    duration = round(len(audio) / 1000, 2)

    # Words per minute
    words = transcript.split()

    if duration > 0:
        wpm = round((len(words) / duration) * 60)
    else:
        wpm = 0

    # Pause detection
    silence = detect_silence(
        audio,
        min_silence_len=700,
        silence_thresh=audio.dBFS - 16
    )

    pauses = len(silence)

    # Count filler words
    fillers = {}
    total_fillers = 0

    lower_text = transcript.lower()

    for word in FILLER_WORDS:

        count = lower_text.count(word)

        if count > 0:
            fillers[word] = count

        total_fillers += count

    # Confidence Score
    confidence = 100

    if wpm < 110:
        confidence -= 10

    if wpm > 170:
        confidence -= 10

    confidence -= pauses * 2
    confidence -= total_fillers * 3

    confidence = max(0, min(confidence, 100))

    # Feedback
    feedback = []

    if wpm < 110:
        feedback.append("Speak a little faster.")
    elif wpm > 170:
        feedback.append("Try speaking a little slower.")
    else:
        feedback.append("Excellent speaking pace.")

    if total_fillers > 5:
        feedback.append("Reduce filler words like 'um' and 'uh'.")
    else:
        feedback.append("Good control over filler words.")

    if pauses > 10:
        feedback.append("Avoid unnecessary long pauses.")
    else:
        feedback.append("Your pauses are well balanced.")

    if confidence >= 90:
        feedback.append("Excellent confidence!")
    elif confidence >= 75:
        feedback.append("Good confidence. Keep practicing.")
    else:
        feedback.append("Practice daily to improve confidence.")

    # Do NOT delete the temporary wav file on Windows.
    # It can cause WinError 32 while Whisper is still using it.

    return {
        "transcript": transcript,
        "duration": duration,
        "wpm": wpm,
        "pauses": pauses,
        "fillers": fillers,
        "confidence": confidence,
        "feedback": feedback
    }