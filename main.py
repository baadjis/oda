import os

import cv2

from app import app

from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from fasterrcnn import object_detection


# allowed image extension
def allowed_image_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_image_extension(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded.jpg')
        file.save(path)
        print(path)
        # print('upload_image filename: ' + filename)
        count_classes = object_detection(path)

        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename='uploaded.jpg', predicted='predicted.jpg',count_classes=count_classes)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    # object_detection_api('static/uploads/'+filename, rect_th=2, text_th=1, text_size=1)

    return redirect(url_for('static', filename='uploads/' + filename), code=301)


"""@app.route('/predicted/<filename>')
def predicted_image(filename):
    # print('display_image filename: ' + filename)
    # object_detection_api('static/uploads/'+filename, rect_th=2, text_th=1, text_size=1)

    return redirect(url_for('static', filename='uploads/' + filename), code=301)

"""
if __name__ == "__main__":
    app.run()
