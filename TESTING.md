# Automated Testing Documentation

## Overview
This project includes comprehensive automated tests for both the Data Access Layer (DAL) and Flask application routes.

## Test Structure

### Unit Tests (`test_dal.py`)
Tests for the Data Access Layer functions:
- Database initialization and table creation
- Project CRUD operations (Create, Read, Delete)
- Data validation and error handling
- Database connection management

### Integration Tests (`test_app.py`)
Tests for Flask application routes:
- All page routes (index, about, resume, projects, contact)
- Form validation and submission
- Session management
- Error handling (404, 500)
- File downloads

## Running Tests

### Prerequisites
Install testing dependencies:
```bash
pip install -r requirements.txt
```

### Basic Test Execution
```bash
# Run all tests
python run_tests.py

# Or run directly with pytest
pytest -v
```

### Coverage Report
```bash
# Run tests with coverage
python run_tests.py --coverage

# Or manually
pytest --cov=. --cov-report=html
```

### Individual Test Files
```bash
# Run only DAL tests
pytest test_dal.py -v

# Run only Flask app tests
pytest test_app.py -v
```

## Test Features

### Database Isolation
- Each test uses a temporary SQLite database
- Tests don't interfere with each other
- No cleanup required after tests

### Mocking
- Database paths are mocked for testing
- File operations are isolated
- Session data is properly managed

### Comprehensive Coverage
- **DAL Tests**: 12 test cases covering all database operations
- **App Tests**: 20+ test cases covering all routes and validation
- **Error Scenarios**: Tests for invalid inputs and edge cases

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Individual function testing
- Database operations
- Data validation

### Integration Tests (`@pytest.mark.integration`)
- Full request/response cycle
- Form submissions
- Session management
- Route handling

## Continuous Integration
The test suite is designed to run in CI/CD pipelines:
- No external dependencies
- Fast execution
- Clear pass/fail indicators
- Detailed error reporting

## Adding New Tests

### For New DAL Functions
1. Add test methods to `TestDAL` class in `test_dal.py`
2. Follow naming convention: `test_function_name_scenario`
3. Use the existing setup/teardown methods

### For New Flask Routes
1. Add test methods to `TestFlaskApp` class in `test_app.py`
2. Test both GET and POST methods if applicable
3. Include validation error scenarios
4. Test redirects and flash messages

## Test Data
- Tests use temporary files and databases
- No real data is modified during testing
- Each test is independent and can run in any order
