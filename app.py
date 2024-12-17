from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import backend  # Import your backend logic

# App configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
# app.secret_key = 'secret_key_for_flask_app'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file is a PDF."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    """Render the file upload form."""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    # Check if file is in the request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # Validate file selection
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash('Allowed file types are PDFs only')
        return redirect(request.url)

    # Save the uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Process the uploaded file using backend logic
    try:
        result = backend.process_resume(file_path)  # Use the backend's modular process_resume
        if not result:
            flash('Failed to process the file.')
            return redirect(request.url)

        # Pass results to the results template
        return render_template(
            'results.html',
            filename=result['file_name'],
            entities=result['entities'],
            skills=result['matched_skills'],
            score=result['score']
        )
    except Exception as e:
        print(f"Error processing the file: {e}")
        flash('An error occurred while processing the file.')
        return redirect(request.url)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
