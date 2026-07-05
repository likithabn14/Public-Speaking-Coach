from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from analyzer import analyze_audio
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "audio" not in request.files:
        return "No audio file uploaded."

    file = request.files["audio"]

    if file.filename == "":
        return "No selected file."

    filename = secure_filename(file.filename)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    result = analyze_audio(filepath)

    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)