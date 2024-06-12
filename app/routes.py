from flask import render_template, request, send_file, url_for
from io import BytesIO
from app import app
from .qr_code.qr_generator import generate_qr
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('url')
    print(data)
    logo = request.files.get('logo_file')
    color = request.form.get('color') if request.form.get('color') else "black"
    print(logo)
    print(color)

    static_folder = os.path.join(app.root_path, 'static')
    
    # Ensure the static directory exists
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
         
    logo_path = None
    if logo:
        logo_filename = 'logo.png'
        logo_path = os.path.join(static_folder, logo_filename)
        logo.save(logo_path)

    qr_code_img = generate_qr(data, logo_path, color)
    
    qr_code_filename = 'generated_qr.png'

    # Save the QR code to a file
    qr_code_path = os.path.join(static_folder, qr_code_filename)
    with open(qr_code_path, 'wb') as f:
        f.write(qr_code_img)

    return render_template('result.html', qr_code_url=url_for('static', filename='generated_qr.png'))

@app.route('/download')
def download():
    return send_file('static/generated_qr.png', as_attachment=True, download_name='qrcode.png')
