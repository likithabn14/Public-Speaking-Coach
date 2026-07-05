import re
from collections import Counter


FILLER_WORDS = [
    "um",
    "uh",
    "umm",
    "uhh",
    "hmm",
    "mmm",
    "like",
    "actually",
    "basically",
    "literally",
    "you know",
    "so",
    "no",
    "not"
]

BAD_WORDS = [
    "fuck",
    "shit",
    "idiot",
    "stupid",
    "damn"
]

GOOD_WORDS = [
    "project",
    "skills",
    "python",
    "sql",
    "machine",
    "learning",
    "team",
    "leadership",
    "experience",
    "internship",
    "goal",
    "opportunity",
    "passionate",
    "developer",
    "engineer"
]


def analyze_text(transcript, duration):

    transcript = transcript.strip()

    words = re.findall(r"\b[\w']+\b", transcript.lower())

    word_count = len(words)

    unique_words = len(set(words))

    if duration <= 0:
        duration = max(5, word_count / 2.5)

    duration_minutes = duration / 60

    if duration_minutes > 0:
        wpm = round(word_count / duration_minutes)
    else:
        wpm = 0

    lower = transcript.lower()

        # -------------------------
    # Speech Length (15)
    # -------------------------

    if word_count < 20:
        length_score = 5
    elif word_count < 50:
        length_score = 10
    elif word_count <= 120:
        length_score = 15
    else:
        length_score = 12

    # -------------------------
    # Speaking Speed (20)
    # -------------------------

    if 110 <= wpm <= 150:
        speed_score = 20
    elif 90 <= wpm < 110:
        speed_score = 15
    elif 151 <= wpm <= 170:
        speed_score = 15
    else:
        speed_score = 8

    # -------------------------
    # Filler Words (15)
    # -------------------------

    fillers = {}

    filler_count = 0

    for word in FILLER_WORDS:

        count = len(
            re.findall(
                r"\b" + re.escape(word) + r"\b",
                lower
            )
        )

        if count > 0:
            fillers[word] = count
            filler_count += count

    if filler_count == 0:
        filler_score = 15
    elif filler_count <= 2:
        filler_score = 12
    elif filler_count <= 5:
        filler_score = 8
    else:
        filler_score = 3

    # -------------------------
    # Vocabulary (15)
    # -------------------------

    ratio = unique_words / word_count if word_count else 0

    if ratio >= 0.70:
        vocab_score = 15
    elif ratio >= 0.55:
        vocab_score = 10
    else:
        vocab_score = 5

    # -------------------------
    # Repeated Words (10)
    # -------------------------

    counts = Counter(words)

    repeated = sum(
        1
        for count in counts.values()
        if count >= 4
    )

    if repeated == 0:
        repeat_score = 10
    elif repeated <= 2:
        repeat_score = 7
    else:
        repeat_score = 4

        # -------------------------
    # Professional Language (10)
    # -------------------------

    professional_score = 10

    for word in BAD_WORDS:
        if word in lower:
            professional_score -= 5

    for word in GOOD_WORDS:
        if word in lower:
            professional_score += 1

    professional_score = max(0, min(10, professional_score))

    # -------------------------
    # Sentence Quality (10)
    # -------------------------

    sentence_count = max(
        transcript.count(".") +
        transcript.count("!") +
        transcript.count("?"),
        1
    )

    avg_sentence = word_count / sentence_count

    if 8 <= avg_sentence <= 20:
        sentence_score = 10
    elif 5 <= avg_sentence < 8 or 21 <= avg_sentence <= 30:
        sentence_score = 7
    else:
        sentence_score = 4

    # -------------------------
    # Confidence (5)
    # -------------------------

    confidence_score = 5

    if filler_count > 3:
        confidence_score -= 2

    if word_count < 20:
        confidence_score -= 2

    confidence_score = max(0, confidence_score)

    # -------------------------
    # Overall Score
    # -------------------------

    overall_score = (
        length_score +
        speed_score +
        filler_score +
        vocab_score +
        repeat_score +
        professional_score +
        sentence_score +
        confidence_score
    )

    # -------------------------
    # Rating & Level
    # -------------------------

    if overall_score >= 90:
        rating = "Excellent ⭐⭐⭐⭐⭐"
        level = "🏆 Expert Speaker"

    elif overall_score >= 80:
        rating = "Very Good ⭐⭐⭐⭐"
        level = "🌟 Advanced Speaker"

    elif overall_score >= 70:
        rating = "Good ⭐⭐⭐"
        level = "👍 Good Speaker"

    elif overall_score >= 60:
        rating = "Average ⭐⭐"
        level = "📈 Improving Speaker"

    else:
        rating = "Needs Improvement ⭐"
        level = "🎯 Beginner Speaker"    

        # -------------------------
    # Strengths & Improvements
    # -------------------------

    strengths = []
    improvements = []

    # Speaking Speed
    if speed_score >= 18:
        strengths.append("Good speaking speed.")
    else:
        improvements.append(
            "Maintain a speaking speed between 110 and 150 WPM."
        )

    # Filler Words
    if filler_score >= 12:
        strengths.append("Very few filler words.")
    else:
        improvements.append(
            "Reduce filler words such as 'um', 'uh', 'mmm' and 'like'."
        )

    # Vocabulary
    if vocab_score >= 12:
        strengths.append("Good vocabulary usage.")
    else:
        improvements.append(
            "Use more varied vocabulary instead of repeating the same words."
        )

    # Professional Language
    if professional_score >= 8:
        strengths.append("Professional language used.")
    else:
        improvements.append(
            "Avoid offensive or informal language in interviews."
        )

    # Speech Length
    if length_score >= 10:
        strengths.append("Good speech length.")
    else:
        improvements.append(
            "Speak for at least 30–60 seconds."
        )

    # Sentence Quality
    if sentence_score >= 8:
        strengths.append("Well-structured sentences.")
    else:
        improvements.append(
            "Use complete sentences with natural pauses."
        )

    if not strengths:
        strengths.append("You completed the speech successfully.")

    # -------------------------
    # Return Results
    # -------------------------

    return {

        "transcript": transcript,

        "duration": round(duration, 1),

        "wpm": wpm,

        "fillers": fillers,

        "overall_score": overall_score,

        "rating": rating,

        "level": level,

        "length_score": length_score,

        "speed_score": speed_score,

        "filler_score": filler_score,

        "vocab_score": vocab_score,

        "repeat_score": repeat_score,

        "professional_score": professional_score,

        "sentence_score": sentence_score,

        "confidence_score": confidence_score,

        "strengths": strengths,

        "improvements": improvements

    }    
