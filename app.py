
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from pathlib import Path

from config import UPLOADS_DIR
from ingest import ingest_pdf
from rag import answer_question

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_document():

    if "file" not in request.files:
        return jsonify({
            "error": "No file selected."
        }), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({
            "error": "Please select a PDF."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF files are supported."
        }), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({
            "error": "Invalid filename."
        }), 400

    filepath = Path(UPLOADS_DIR) / filename

    file.save(filepath)

    try:

        result = ingest_pdf(filepath)

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 400


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    compare = data.get("compare", False)

    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    try:

        rag_result = answer_question(
            question,
            use_rag=True
        )

        response = {
            "rag": rag_result
        }

        if compare:

            normal_result = answer_question(
                question,
                use_rag=False
            )

            response["without_rag"] = normal_result

        return jsonify(response)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
