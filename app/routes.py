import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from app import db
from app.models import Report, User

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        category = request.form.get('category')
        street = request.form.get('street')
        description = request.form.get('description')
        reporter_name = request.form.get('reporter_name')
        reporter_cell = request.form.get('reporter_cell')
        
        reference = Report.generate_reference()
        
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = filename.rsplit('.', 1)[1].lower()
                    new_filename = f"{reference}.{extension}"
                    
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    file.save(os.path.join(upload_folder, new_filename))
                    photo_path = new_filename
                else:
                    flash('Invalid file type. Only JPG, PNG, and WEBP are allowed.', 'danger')
                    return redirect(url_for('main.report'))

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
            return render_template('success.html', reference=reference)
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving the report. Please try again.', 'danger')
            print(e)

    return render_template('report.html')

@main.route('/check_status', methods=['GET', 'POST'])
def check_status():
    report = None
    error = None
    
    if request.method == 'POST':
        reference_input = request.form.get('reference').strip().upper()
        report = Report.query.filter_by(reference=reference_input).first()
        
        if not report:
            error = f"No report found with reference number '{reference_input}'. Please check and try again."
            
    return render_template('check_status.html', report=report, error=error)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard')) # Now redirects to the dashboard
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('main.login'))
    
    # Get all reports (newest first)
    reports = Report.query.order_by(Report.created_at.desc()).all()
    
    # Analytics: Count by Category
    category_counts = db.session.query(Report.category, db.func.count(Report.id)).group_by(Report.category).all()
    
    # Analytics: Count by Status
    status_counts = db.session.query(Report.status, db.func.count(Report.id)).group_by(Report.status).all()
    
    return render_template('dashboard.html', reports=reports, category_counts=category_counts, status_counts=status_counts)

@main.route('/update_status/<int:report_id>', methods=['POST'])
def update_status(report_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    new_status = request.form.get('status')
    report = Report.query.get_or_404(report_id)
    
    if new_status in ['Open', 'In progress', 'Closed']:
        report.status = new_status
        db.session.commit()
        flash(f'Status for {report.reference} updated to {new_status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
        
    return redirect(url_for('main.dashboard'))