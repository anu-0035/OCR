from PIL import Image
import pytesseract
import cv2
from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Specify the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def ocr_core(image):
    text = pytesseract.image_to_string(Image.fromarray(image))
    return text

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    processed_image = preprocess_image(file_path)
    text = ocr_core(processed_image)
    
    return f"Recognized Text: {text}"

if __name__ == "__main__":
    app.run(debug=True)