from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from collections import Counter
from colormap import rgb2hex

app = Flask(__name__)


def process_image(image):
    img = Image.open(image)
    img = img.convert("RGB")
    img = img.resize((150, 150))
    img_array = np.array(img)
    img_array = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))
    return img_array


def find_most_common_colors(img_array):
    counter = Counter(map(tuple, img_array))
    most_common = counter.most_common(10)  # Get the 10 most common colors
    return most_common


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == "":
            return render_template("index.html", error="No file uploaded")
        filename = secure_filename(file.filename)
        file.save(f'path_to_where_file_should _be_saved{filename}')

        img_array = process_image(file)
        most_common_colors = find_most_common_colors(img_array)
        hex_color = []
        for color in most_common_colors:
            hex_ = f'hexcode:{rgb2hex(color[0][0],color[0][1],color[0][2])}'
            hex_color.append(hex_)
        return render_template('index.html', image=True, most_common_colors=most_common_colors, hex_color=hex_color)

    return render_template('index.html', error='No file uploaded')


if __name__ == "__main__":
    app.run(debug=True)