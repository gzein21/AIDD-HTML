import pytest
import os
import tempfile
import sqlite3
from unittest.mock import patch, MagicMock
from DAL import init_db, list_projects, insert_project, delete_project, get_connection, get_db_path


class TestDAL:
    """Test cases for Data Access Layer functions"""
    
    def setup_method(self):
        """Set up test database before each test"""
        # Create a temporary database file for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        
        # Patch the get_db_path function to use our test database
        self.db_path_patcher = patch('DAL.get_db_path')
        self.mock_db_path = self.db_path_patcher.start()
        self.mock_db_path.return_value = self.test_db_path
        
        # Initialize the test database
        init_db()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.db_path_patcher.stop()
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)
    
    def test_init_db_creates_table(self):
        """Test that init_db creates the projects table"""
        with get_connection() as conn:
            cur = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='projects'"
            )
            result = cur.fetchone()
            assert result is not None
            assert result[0] == 'projects'
    
    def test_init_db_table_structure(self):
        """Test that the projects table has correct structure"""
        with get_connection() as conn:
            cur = conn.execute("PRAGMA table_info(projects)")
            columns = cur.fetchall()
            
            column_names = [col[1] for col in columns]
            expected_columns = ['id', 'title', 'description', 'image_file_name', 'created_at']
            
            for expected_col in expected_columns:
                assert expected_col in column_names
    
    def test_insert_project_success(self):
        """Test successful project insertion"""
        project_id = insert_project("Test Project", "Test Description", "test.jpg")
        
        assert project_id is not None
        assert isinstance(project_id, int)
        
        # Verify the project was inserted
        projects = list_projects()
        assert len(projects) == 1
        assert projects[0]['title'] == "Test Project"
        assert projects[0]['description'] == "Test Description"
        assert projects[0]['image_file_name'] == "test.jpg"
    
    def test_insert_project_strips_whitespace(self):
        """Test that insert_project strips whitespace from inputs"""
        project_id = insert_project("  Test Project  ", "  Test Description  ", "  test.jpg  ")
        
        projects = list_projects()
        assert projects[0]['title'] == "Test Project"
        assert projects[0]['description'] == "Test Description"
        assert projects[0]['image_file_name'] == "test.jpg"
    
    def test_list_projects_empty(self):
        """Test list_projects returns empty list when no projects exist"""
        projects = list_projects()
        assert projects == []
    
    def test_list_projects_multiple(self):
        """Test list_projects returns multiple projects in correct order"""
        # Insert multiple projects
        insert_project("Project 1", "Description 1", "image1.jpg")
        insert_project("Project 2", "Description 2", "image2.jpg")
        insert_project("Project 3", "Description 3", "image3.jpg")
        
        projects = list_projects()
        assert len(projects) == 3
        
        # Should be ordered by created_at DESC (newest first)
        assert projects[0]['title'] == "Project 3"
        assert projects[1]['title'] == "Project 2"
        assert projects[2]['title'] == "Project 1"
    
    def test_delete_project_success(self):
        """Test successful project deletion"""
        # Insert a project first
        project_id = insert_project("Test Project", "Test Description", "test.jpg")
        
        # Delete the project
        deleted_count = delete_project(project_id)
        
        assert deleted_count == 1
        
        # Verify project is gone
        projects = list_projects()
        assert len(projects) == 0
    
    def test_delete_project_nonexistent(self):
        """Test deleting a non-existent project"""
        deleted_count = delete_project(999)  # Non-existent ID
        assert deleted_count == 0
    
    def test_delete_project_multiple(self):
        """Test deleting one project from multiple"""
        # Insert multiple projects
        project_id1 = insert_project("Project 1", "Description 1", "image1.jpg")
        project_id2 = insert_project("Project 2", "Description 2", "image2.jpg")
        
        # Delete one project
        deleted_count = delete_project(project_id1)
        assert deleted_count == 1
        
        # Verify only one project remains
        projects = list_projects()
        assert len(projects) == 1
        assert projects[0]['id'] == project_id2
    
    def test_get_connection_row_factory(self):
        """Test that get_connection returns connection with row factory"""
        conn = get_connection()
        assert conn.row_factory == sqlite3.Row
        conn.close()
    
    def test_get_db_path(self):
        """Test get_db_path returns correct path"""
        with patch('DAL.os.path.join') as mock_join:
            mock_join.return_value = '/test/path/projects.db'
            path = get_db_path()
            assert path == '/test/path/projects.db'
            mock_join.assert_called_once()
