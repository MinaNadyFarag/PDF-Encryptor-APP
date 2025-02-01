from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO  # Import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB file size limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def encrypt_pdf(input_pdf, password):
    """Encrypt the PDF with a password."""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Encrypt the PDF with the password
    writer.encrypt(user_password=password, owner_password=None, use_128bit=True)
    return writer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file and password
        file = request.files['file']
        password = request.form['password']

        if file and password:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Encrypt the PDF
            encrypted_pdf = encrypt_pdf(file_path, password)

            # Save the encrypted PDF to a BytesIO object
            output = BytesIO()
            encrypted_pdf.write(output)
            output.seek(0)

            # Return the file for download
            return send_file(
                output,
                as_attachment=True,
                download_name="encrypted.pdf",
                mimetype="application/pdf"
            )

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)