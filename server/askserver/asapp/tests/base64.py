from django.test import TestCase
from asapp.b64url_enhancement import check_base64

# Generated with the help of ChatGPT 3.5,
# https://chat.openai.com/share/f7a9c685-b0c3-4455-ab18-312d4b5ac1c2

class Base64TestCase(TestCase):
    def test_valid_base64(self):
        # Test valid base64 encoded string
        text = "VGhpcyBpcyBhIHRlc3QgZW5jb2RlZCBzdHJpbmc"
        self.assertTrue(check_base64(text))

    def test_invalid_base64(self):
        # Test invalid base64 encoded string
        text = "This is not a valid base64 encoded string"
        self.assertFalse(check_base64(text))

    def test_empty_string(self):
        # Test empty string
        text = ""
        self.assertTrue(check_base64(text))

    def test_non_string_input(self):
        # Test non-string input
        text = 12345
        with self.assertRaises(TypeError):
            check_base64(text)

    def test_unicode_string(self):
        # Test unicode string
        text = "VGhpcyBpcyBhIHRlc3QgZW5jb2RlZCBzdHJpbmc=".encode('utf-8')
        self.assertTrue(check_base64(text.decode('utf-8')))

    def test_long_base64(self):
        # Test long base64 encoded string
        text = "VGhpcyBpcyBhIHRlc3QgZW5jb2RlZCBzdHJpbmc" + "a"*1000
        self.assertFalse(check_base64(text))

    def test_short_base64(self):
        # Test short base64 encoded string
        text = "VGhpcw=="
        self.assertTrue(check_base64(text))

    def test_special_characters(self):
        # Test base64 encoded string with special characters
        text = "VGhpcyBpcyBhIHRl!c3QgZW5jb2RlZCBzdHJpbmc="
        self.assertFalse(check_base64(text))
