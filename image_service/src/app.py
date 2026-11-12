#Written by: Christina Rusu
#Date: 11/10/2026

from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image
from pathlib import Path
import random

app = Flask(__name__)

FOLDER = Path(__file__).resolve().parent.parent  # finds the base folder
UPLOADS = FOLDER / "uploads"  
RESIZED = FOLDER / "resized"
DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500

# verifies that uploads amd resized folders exist
UPLOADS.mkdir(exist_ok=True)  
RESIZED.mkdir(exist_ok=True)

FILE_TYPES = ["jpeg", "jpg", "png"]

# function verifies that file type is allowed
def file_type(file):
    if "." in file and file.rsplit(".", 1)[1].lower() in FILE_TYPES:
        return True
    else:
        return False

#opens test program:
@app.route("/")
def test_page():
    return render_template("imgtest.html")

# Upload images
@app.route("/images", methods=["POST"])
def upload_img():
    if "file" not in request.files:
        return jsonify({"error": "No image added"}), 400
    file = request.files["file"]
    if not file.filename or not file_type(file.filename):
        return jsonify({"error": "Only JPG and PNG file types allowed!"}), 400
    
    # ensures a unique 5 digit ID is assigned to the image
    while True:
        img_id = str(random.randint(10000, 99999))
        existing_image = any(
            (folder / f"{img_id}.{type}").exists()
            for folder in [UPLOADS, RESIZED]
            for type in FILE_TYPES
        )
        if not existing_image:
            break

    img_ext = file.filename.rsplit(".", 1)[1].lower()  # obtains file type (JPG or PNG)
    img_path = UPLOADS / f"{img_id}.{img_ext}"
    resized_path = RESIZED / f"{img_id}.{img_ext}"

    try:
        img = Image.open(file.stream)
        img.verify()
        file.stream.seek(0)
        img = Image.open(file.stream)
        img.save(img_path)
        img.thumbnail((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        img.save(resized_path)
    except Exception:
        return jsonify ({"error": "invalid image file type!"}), 400
    return jsonify({
        "imageID": img_id,
        "message": "Image has been successfully uploaded",
        "imagePath": f"uploads/{img_id}.{img_ext}"
        }), 201

# Retrieve image
@app.route("/images/<img_id>", methods=["GET"])
def getImg(img_id):
    if not img_id.isdigit() or len(img_id) != 5:
        return jsonify({"error": "Invalid image ID"}), 400

    for type in FILE_TYPES:
        img_name = f"{img_id}.{type}"

        if (UPLOADS / img_name).exists():
            return send_from_directory(UPLOADS, img_name), 200

    return jsonify({"error": "Image not found"}), 404

# Image deletion
@app.route("/images/<img_id>", methods=["DELETE"])
def delete_image(img_id):

    if not img_id.isdigit() or len(img_id) != 5:
        return jsonify({"error": "Invalid image ID"}), 400

    found = False

    for folder in [UPLOADS, RESIZED]:
        for type in FILE_TYPES:
            image_path = folder / f"{img_id}.{type}"

            if image_path.exists():
                image_path.unlink()
                found = True

    if not found:
        return jsonify({"error": "Image not found"}), 404

    return jsonify({
        "imageID": img_id,
        "message": "Image deleted successfully"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)