from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
from datetime import datetime
from DAL import init_db, list_projects, insert_project, delete_project

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# Ensure DB exists at startup
init_db()

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/resume')
def resume():
    """Resume page route"""
    return render_template('resume.html')

@app.route('/projects')
def projects():
    """Projects page route"""
    projects_rows = list_projects()
    return render_template('projects.html', projects=projects_rows)

@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_file_name = request.form.get('image_file_name', '').strip()

        errors = []
        if not title:
            errors.append('Title is required')
        if not description:
            errors.append('Description is required')
        if not image_file_name:
            errors.append('Image file name is required (place image in static/images)')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('project_form.html')

        insert_project(title, description, image_file_name)
        flash('Project added successfully', 'success')
        return redirect(url_for('projects'))

    return render_template('project_form.html')

@app.route('/projects/delete/<int:project_id>', methods=['POST'])
def delete_project_route(project_id: int):
    deleted_count = delete_project(project_id)
    if deleted_count:
        flash('Project deleted', 'success')
    else:
        flash('Project not found', 'error')
    return redirect(url_for('projects'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route with form handling"""
    if request.method == 'POST':
       
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        
        errors = []
        
        if len(first_name) < 2:
            errors.append('First name must be at least 2 characters long')
        
        if len(last_name) < 2:
            errors.append('Last name must be at least 2 characters long')
        
        if not email or '@' not in email:
            errors.append('Please enter a valid email address')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if len(subject) < 5:
            errors.append('Subject must be at least 5 characters long')
        
        if len(message) < 10:
            errors.append('Message must be at least 10 characters long')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html')
        
        # Store form data in session for thank you page
        session['form_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'subject': subject,
            'message': message,
            'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        
        
        flash('Thank you for your message! I\'ll get back to you soon.', 'success')
        return redirect(url_for('thank_you'))
    
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    """Thank you page route"""
    form_data = session.get('form_data')
    if not form_data:
        flash('No form data found. Please submit the contact form first.', 'error')
        return redirect(url_for('contact'))
    
    return render_template('thankyou.html', form_data=form_data)

@app.route('/download-resume')
def download_resume():
    """Route to serve resume PDF"""
    return send_file('Zein_George_Resume.pdf', as_attachment=True)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
