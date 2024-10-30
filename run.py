import unittest
from app import create_app
from tests.function_testing import TestUserManagement

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


