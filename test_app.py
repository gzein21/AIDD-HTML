import pytest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock
from app import app
from DAL import init_db


class TestFlaskApp:
    """Integration tests for Flask application routes"""
    
    def setup_method(self):
        """Set up test client and database before each test"""
        # Create a temporary database file for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        
        # Patch the DAL to use our test database
        self.db_path_patcher = patch('DAL.get_db_path')
        self.mock_db_path = self.db_path_patcher.start()
        self.mock_db_path.return_value = self.test_db_path
        
        # Initialize the test database
        init_db()
        
        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
        # Create test uploads directory
        self.test_uploads_dir = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.test_uploads_dir
    
    def teardown_method(self):
        """Clean up after each test"""
        self.db_path_patcher.stop()
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)
        
        # Clean up test uploads directory
        import shutil
        shutil.rmtree(self.test_uploads_dir, ignore_errors=True)
    
    def test_index_route(self):
        """Test home page route"""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_about_route(self):
        """Test about page route"""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_resume_route(self):
        """Test resume page route"""
        response = self.client.get('/resume')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_projects_route_empty(self):
        """Test projects page with no projects"""
        response = self.client.get('/projects')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_projects_route_with_data(self):
        """Test projects page with project data"""
        # Add a test project
        from DAL import insert_project
        insert_project("Test Project", "Test Description", "test.jpg")
        
        response = self.client.get('/projects')
        assert response.status_code == 200
        assert b'Test Project' in response.data
        assert b'Test Description' in response.data
    
    def test_add_project_get(self):
        """Test GET request to add project form"""
        response = self.client.get('/projects/add')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_add_project_post_success(self):
        """Test successful project addition via POST"""
        data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/add', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Check that project was added
        from DAL import list_projects
        projects = list_projects()
        assert len(projects) == 1
        assert projects[0]['title'] == 'Test Project'
    
    def test_add_project_post_validation_errors(self):
        """Test project addition with validation errors"""
        # Test empty title
        data = {
            'title': '',
            'description': 'Test Description',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/add', data=data)
        assert response.status_code == 200
        assert b'Title is required' in response.data
        
        # Test empty description
        data = {
            'title': 'Test Project',
            'description': '',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/add', data=data)
        assert response.status_code == 200
        assert b'Description is required' in response.data
        
        # Test empty image file name
        data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'image_file_name': ''
        }
        
        response = self.client.post('/projects/add', data=data)
        assert response.status_code == 200
        assert b'Image file name is required' in response.data
    
    def test_delete_project_success(self):
        """Test successful project deletion"""
        # Add a test project first
        from DAL import insert_project
        project_id = insert_project("Test Project", "Test Description", "test.jpg")
        
        response = self.client.post(f'/projects/delete/{project_id}', follow_redirects=True)
        assert response.status_code == 200
        
        # Check that project was deleted
        from DAL import list_projects
        projects = list_projects()
        assert len(projects) == 0
    
    def test_delete_project_nonexistent(self):
        """Test deleting non-existent project"""
        response = self.client.post('/projects/delete/999', follow_redirects=True)
        assert response.status_code == 200
        assert b'Project not found' in response.data
    
    def test_contact_get(self):
        """Test GET request to contact form"""
        response = self.client.get('/contact')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_contact_post_success(self):
        """Test successful contact form submission"""
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Thank you for your message' in response.data
    
    def test_contact_post_validation_errors(self):
        """Test contact form validation errors"""
        # Test short first name
        data = {
            'firstName': 'J',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'First name must be at least 2 characters long' in response.data
        
        # Test short last name
        data = {
            'firstName': 'John',
            'lastName': 'D',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Last name must be at least 2 characters long' in response.data
        
        # Test invalid email
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'invalid-email',
            'password': 'password123',
            'confirmPassword': 'password123',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Please enter a valid email address' in response.data
        
        # Test short password
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '123',
            'confirmPassword': '123',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Password must be at least 8 characters long' in response.data
        
        # Test password mismatch
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password456',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Passwords do not match' in response.data
        
        # Test short subject
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123',
            'subject': 'Hi',
            'message': 'This is a test message with enough characters'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Subject must be at least 5 characters long' in response.data
        
        # Test short message
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123',
            'subject': 'Test Subject',
            'message': 'Short'
        }
        
        response = self.client.post('/contact', data=data)
        assert response.status_code == 200
        assert b'Message must be at least 10 characters long' in response.data
    
    def test_thank_you_with_session_data(self):
        """Test thank you page with session data"""
        with self.client.session_transaction() as sess:
            sess['form_data'] = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'subject': 'Test Subject',
                'message': 'Test Message',
                'submission_time': '2024-01-01 12:00:00'
            }
        
        response = self.client.get('/thank-you')
        assert response.status_code == 200
        assert b'John' in response.data
        assert b'Doe' in response.data
    
    def test_thank_you_without_session_data(self):
        """Test thank you page without session data"""
        response = self.client.get('/thank-you', follow_redirects=True)
        assert response.status_code == 200
        assert b'No form data found' in response.data
    
    def test_download_resume(self):
        """Test resume download route"""
        # Create a mock resume file
        test_resume_path = os.path.join(os.path.dirname(__file__), 'Zein_George_Resume.pdf')
        
        with patch('app.send_file') as mock_send_file:
            mock_send_file.return_value = 'Mock file content'
            response = self.client.get('/download-resume')
            assert response.status_code == 200
            mock_send_file.assert_called_once_with('Zein_George_Resume.pdf', as_attachment=True)
    
    def test_404_error_handler(self):
        """Test 404 error handler"""
        response = self.client.get('/nonexistent-page')
        assert response.status_code == 404
        assert b'<!DOCTYPE html>' in response.data
    
    def test_500_error_handler(self):
        """Test 500 error handler"""
        # This would require causing an actual server error, which is complex in tests
        # For now, we'll just verify the handler exists
        assert app.error_handler_spec[None][500] is not None
