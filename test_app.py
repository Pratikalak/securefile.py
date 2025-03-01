import unittest
import hashlib
import base64
import os

class TestSecureFileVault(unittest.TestCase):
    def setUp(self):
        """Setup test environment"""
        self.test_text = "Hello World!"
        self.test_pin = 1234
        self.test_email = "test@example.com"
        self.test_password = "Test123@"

    def test_password_hashing(self):
        """Test password hashing functionality"""
        password = self.test_password.encode()
        hashed = hashlib.sha256(password).hexdigest()
        self.assertEqual(len(hashed), 64)  # SHA-256 produces 64 character hex string
        self.assertTrue(isinstance(hashed, str))

    def test_base64_encoding(self):
        """Test base64 encoding/decoding"""
        encoded = base64.b64encode(self.test_text.encode()).decode()
        decoded = base64.b64decode(encoded.encode()).decode()
        self.assertEqual(decoded, self.test_text)

    def test_email_validation(self):
        """Test email validation pattern"""
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        self.assertTrue(email_pattern.match(self.test_email))
        self.assertFalse(email_pattern.match("invalid.email"))

    def test_password_validation(self):
        """Test password validation pattern"""
        import re
        password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,24}$')
        self.assertTrue(password_pattern.match(self.test_password))
        self.assertFalse(password_pattern.match("weak"))

    def test_file_operations(self):
        """Test basic file operations"""
        test_file = "test.txt"
        # Write test
        with open(test_file, "w") as f:
            f.write(self.test_text)
        # Read test
        with open(test_file, "r") as f:
            content = f.read()
        self.assertEqual(content, self.test_text)
        # Cleanup
        os.remove(test_file)

    def test_online_file_dir_exists(self):
        """Test if online_file directory exists"""
        dir_path = os.path.join(os.path.dirname(__file__), "online_file")
        self.assertTrue(os.path.exists(dir_path))

if __name__ == '__main__':
    unittest.main(verbosity=2)
