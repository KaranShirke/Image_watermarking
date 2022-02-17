from flask import Flask, render_template, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename

from skimage.metrics import structural_similarity
import imutils
import cv2
import numpy as np
from PIL import Image


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "asphalt8"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 *1024

ALLOWED_EXTENSIONS = set(['png', 'jpg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def upload_image():
    if request.method == "POST":
        option = request.form['options']
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)
        image_logow = np.array(image.convert('RGB'))
        h_image, w_image, _ = image_logow.shape
        
        if option == 'logo_watermark':
            logo_upload = request.files['logo_upload']
            logoname = logo_upload.filename
            logo = Image.open(logo_upload)
            logo = np.array(logo.convert('RGB'))
            h_logo, w_logo, _ = logo.shape
            center_y = int(h_image / 2)
            center_x = int(w_image / 2)
            top_y = center_y - int(h_logo / 2)
            left_x = center_x - int(w_logo / 2)
            bottom_y = top_y + h_logo
            right_x = left_x + w_logo
            
            roi = image_logow[top_y: bottom_y, left_x: right_x]
            result = cv2.addWeighted(roi, 1, logo, 1, 0)
            cv2.line(image_logow, (0, center_y), (left_x, center_y), (0, 0, 255), 1)
            cv2.line(image_logow, (right_x, center_y), (w_image, center_y), (0, 0, 255), 1)
            image_logow[top_y: bottom_y, left_x: right_x] = result
            
            img = Image.fromarray(image_logow, 'RGB')
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.png'))
            full_filename =  'static/uploads/image.png'
            return render_template('index.html', full_filename = full_filename)
            
        else:
            text_mark = request.form['text_watermark']
            
            cv2.putText(image_logow, text=text_mark, org=(w_image - 200, h_image - 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
            color=(0,0,255), thickness=1, lineType=cv2.LINE_4); 
            timg = Image.fromarray(image_logow, 'RGB')
            timg.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.png'))
            full_filename =  'static/uploads/image.png'
            return render_template('index.html', full_filename = full_filename)

if __name__ == "__main__":
    app.run()

