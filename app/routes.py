import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Report

main = Blueprint('main', __name__)

# Helper function to check if the uploaded file is allowed (Part E requirement)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # 1. Get the form data
        category = request.form.get('category')
        street = request.form.get('street')
        description = request.form.get('description')
        reporter_name = request.form.get('reporter_name')
        reporter_cell = request.form.get('reporter_cell')
        
        # 2. Generate reference number
        reference = Report.generate_reference()
        
        # 3. Handle the photo upload (Part E)
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                if allowed_file(file.filename):
                    # Secure the filename and rename it to the reference number (e.g., W42-0001.jpg)
                    filename = secure_filename(file.filename)
                    extension = filename.rsplit('.', 1)[1].lower()
                    new_filename = f"{reference}.{extension}"
                    
                    # Save the file to the uploads folder
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    file.save(os.path.join(upload_folder, new_filename))
                    
                    # Save just the path to the database, not the image itself
                    photo_path = new_filename
                else:
                    flash('Invalid file type. Only JPG, PNG, and WEBP are allowed.', 'danger')
                    return redirect(url_for('main.report'))

        # 4. Save to the database
        new_report = Report(
            reference=reference,
            category=category,
            street=street,
            description=description,
            reporter_name=reporter_name,
            reporter_cell=reporter_cell,
            photo_path=photo_path,
            status='Open'
        )
        
        try:
            db.session.add(new_report)
            db.session.commit()
            # Redirect to the success page, passing the reference number
            return render_template('success.html', reference=reference)
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving the report. Please try again.', 'danger')
            print(e)

    return render_template('report.html')