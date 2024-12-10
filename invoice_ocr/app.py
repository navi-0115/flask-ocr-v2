from flask import Flask, request, jsonify
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

UPLOAD_FOLDER = './invoice_ocr/uploads'
TEXT_FOLDER = './invoice_ocr/extracted_text'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

@app.route('/ocr', methods=['POST'])
def process_pdf():
    try:
        # Check file exists
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        pdf_file = request.files['file']

        # Save pdf file
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(pdf_path)

        # Convert pdf to images
        images = convert_from_path(pdf_path)
        image_paths = []

        for i, page in enumerate(images):
            image_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename.replace('.pdf', f'_page_{i + 1}.jpg'))
            page.save(image_path, 'JPEG')
            image_paths.append(image_path)

        # OCR
        combined_text = ""
        for i, image_path in enumerate(image_paths):
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            combined_text += f"Page {i + 1}:\n{text}\n"

        # Save extracted text
        text_file_path = os.path.join(TEXT_FOLDER, pdf_file.filename.replace('.pdf', '.txt'))
        with open(text_file_path, 'w') as text_file:
            text_file.write(combined_text)

        return jsonify({
            "message": "OCR process completed successfully",
            "text_file_path": text_file_path,
            "extracted_text": combined_text,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500