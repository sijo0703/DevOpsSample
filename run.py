import unittest
from app import create_app
from tests.test_02_function import TestUserManagement

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


