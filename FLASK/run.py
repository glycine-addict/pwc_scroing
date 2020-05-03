from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "uploaded_files"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 16 megabytes, raises RequestEntityTooLarge
# TODO: consider handling the exception
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


@app.route('/upload', methods = ["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        # as a test, accept only txt files
        if not f.filename.endswith(".txt"):
            return "uploaded file wasn't a txt"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return "file uploaded successfully with name " + f.filename


@app.route('/')
def hello():
    return render_template("index.html")


if __name__ == '__main__':
    pass
