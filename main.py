from flask import Flask, render_template, request
from PIL import Image
from pyembroidery import EmbPattern, write_dst, write_dse
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

STITCH_THRESHOLD = 128
STITCH_SPACING = 2

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['image']
    if file:
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        image = Image.open(path).convert("L")
        width, height = image.size

        pattern = EmbPattern()
        for y in range(0, height, STITCH_SPACING):
            for x in range(0, width, STITCH_SPACING):
                if image.getpixel((x, y)) < STITCH_THRESHOLD:
                    pattern.add_stitch_absolute(x, y)

        base_name = path.rsplit(".", 1)[0]
        dst_file = base_name + ".dst"
        dse_file = base_name + ".dse"

        write_dst(pattern, dst_file)
        write_dse(pattern, dse_file)

        return render_template("index.html", download_link_dst=dst_file, download_link_dse=dse_file)

    return "لم يتم رفع الصورة"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
