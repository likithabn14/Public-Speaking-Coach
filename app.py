from flask import Flask, render_template, request
from analyzer import analyze_text

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    transcript = request.form.get("transcript", "").strip()

    try:
        duration = float(request.form.get("duration", 0))
    except ValueError:
        duration = 0

    result = analyze_text(transcript, duration)

    return render_template(
        "result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
