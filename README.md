# George Zein - Portfolio Flask Application

A modern Flask web application showcasing George Zein's professional portfolio, featuring his expertise in MSIS, process automation, ERP systems, and corporate finance experience at Eaton Corporation.

## Features

- **Responsive Design**: Modern, mobile-friendly interface with clean styling
- **Dynamic Navigation**: Flask-powered routing with Jinja2 templating
- **Contact Form**: Fully functional contact form with client-side and server-side validation
- **Professional Portfolio**: Comprehensive showcase of projects, experience, and skills
- **Resume Download**: Direct PDF download functionality
- **Error Handling**: Custom 404 and 500 error pages
- **Flash Messages**: User feedback system for form submissions

## Project Structure

```
AIDD HTML/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── Zein_George_Resume.pdf # Resume PDF
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── contact.html      # Contact page with form
│   ├── projects.html     # Projects showcase
│   ├── resume.html       # Resume page
│   ├── thankyou.html     # Thank you page
│   ├── 404.html          # Not found error page
│   └── 500.html          # Server error page
├── css/                  # Stylesheets
│   └── styles.css        # Main stylesheet
├── images/               # Image assets
│   └── IMG_1359.jpeg     # Profile photo
└── uploads/               # File upload directory
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   # If you have git
   git clone <repository-url>
   cd AIDD-HTML
   
   # Or simply navigate to the project directory
   cd "C:\Users\georg\Downloads\AIDD HTML"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The portfolio should be running!

## Usage

### Running the Application

The Flask application runs in debug mode by default, which means:
- Automatic reloading when code changes
- Detailed error messages
- Accessible from any device on your network

### Development Mode

```bash
python app.py
```

### Production Mode

For production deployment, you should:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Set up proper environment variables for the secret key

## Features Overview

### Pages

- **Home (`/`)**: Welcome page with overview and navigation
- **About (`/about`)**: Detailed background, interests, and goals
- **Projects (`/projects`)**: Showcase of professional projects
- **Resume (`/resume`)**: Professional experience and skills
- **Contact (`/contact`)**: Contact form and information
- **Thank You (`/thank-you`)**: Confirmation page after form submission

### Contact Form

The contact form includes:
- Client-side validation with JavaScript
- Server-side validation with Flask
- Real-time error feedback
- Form data persistence across sessions
- Professional thank you page

### Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## Customization

### Updating Content

1. **Personal Information**: Edit the templates in the `templates/` directory
2. **Styling**: Modify `css/styles.css`
3. **Images**: Replace files in the `images/` directory
4. **Resume**: Update `Zein_George_Resume.pdf`

### Adding New Pages

1. Create a new template in `templates/`
2. Add a route in `app.py`
3. Update navigation in `templates/base.html`

### Modifying Styling

The CSS uses a consistent color scheme:
- Primary Red: `#C8102E`
- Dark Red: `#8B0000`
- Background: `#f8f9fa`

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

For production, consider using:
- **Heroku**: Easy deployment with git integration
- **DigitalOcean**: VPS deployment
- **AWS**: Scalable cloud deployment
- **PythonAnywhere**: Simple Python hosting

### Environment Variables

For production, set these environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `app.py`: `app.run(port=5001)`

2. **Module not found errors**
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Static files not loading**
   - Check file paths in templates
   - Verify files exist in `static/` directory

4. **Form not submitting**
   - Check browser console for JavaScript errors
   - Verify Flask routes are working

### Debug Mode

Debug mode is enabled by default. To disable:
```python
# In app.py, change:
app.run(debug=True, host='0.0.0.0', port=5000)
# To:
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating**: Jinja2
- **Styling**: Custom CSS with responsive design
- **Form Handling**: Flask-WTF (form validation)

## Contact

For questions about this Flask application or portfolio:

- **Email**: gzein@iu.edu
- **LinkedIn**: [linkedin.com/in/georgezeiniu](https://linkedin.com/in/georgezeiniu)
- **GitHub**: [github.com/gzein21](https://github.com/gzein21)

## License

This project is for portfolio purposes. All rights reserved.

---

**Note**: This Flask application was converted from a static HTML portfolio to provide dynamic functionality, form handling, and better maintainability.
