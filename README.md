# Human Background Remover

This project is a web application that allows users to upload images, remove the background using machine learning, and download the processed image with a transparent background in PNG format.

## Features
- Upload an image and remove its background.
- Download the processed image with a transparent background.
- Preview both the original and the background-removed images.
- Supports PNG download for easy integration into other applications.

## How It Works
The application uses [Mediapipe](https://mediapipe.dev) for human segmentation and OpenCV to process the image and remove the background. 

### Steps:
1. The user uploads an image.
2. The app processes the image using Mediapipe’s segmentation model to detect the human figure.
3. The background is removed and replaced with transparency (alpha channel).
4. The user can download the image in PNG format.

## Getting Started

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Flask
- OpenCV
- Mediapipe

You can install the required packages using:
```bash
pip install -r requirements.txt





How to Run the Project
### Steps:
# 1. Clone the repository to your local machine:
   
     git clone https://github.com/kunal0230/human_background_remover.git
      cd human_background_remover


# 2. Navigate into the project directory
  
    cd human_background_remover
# 3. Install Install Required Dependencies:

    pip install -r requirements.txt
# 4. Start the Flask Development Server:
    python app.py
# 5. Usage Instructions in the Browser:
    Once the server is running, open your browser and navigate to
     http://127.0.0.1:5000/
