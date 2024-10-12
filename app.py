import os
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize Mediapipe's segmentation model
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmenter = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Set the upload folder
UPLOAD_FOLDER = 'static/uploads'  # Updated to store files in static folder for serving
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home route to render the upload form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the image upload and background removal
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))

    if file:
        # Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Perform background removal and save PNG with transparent background
        transparent_image = remove_background(filepath)

        # Save the result image with transparency
        transparent_filepath = os.path.join(UPLOAD_FOLDER, 'transparent_' + file.filename.split('.')[0] + '.png')
        cv2.imwrite(transparent_filepath, transparent_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])

        # Render both the original and processed image
        return render_template('index.html', original_image=url_for('static', filename='uploads/' + file.filename),
                               output_image=url_for('static', filename='uploads/' + 'transparent_' + file.filename.split('.')[0] + '.png'))


# Function to remove the background using Mediapipe
# Function to remove the background and produce transparent PNG
def remove_background(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform segmentation
    result = segmenter.process(rgb_image)
    mask = result.segmentation_mask

    # Apply Gaussian blur to the mask to smooth the edges
    blurred_mask = cv2.GaussianBlur(mask, (15, 15), 0)

    # Create the condition mask for transparency
    condition = blurred_mask > 0.5

    # Prepare the output image with alpha channel (RGBA)
    transparent_image = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

    # Copy the original image where the mask is True, and set alpha to 255
    transparent_image[condition] = np.concatenate([image[condition], np.full((np.sum(condition), 1), 255)], axis=-1)

    return transparent_image


if __name__ == '__main__':
    app.run(debug=True)
