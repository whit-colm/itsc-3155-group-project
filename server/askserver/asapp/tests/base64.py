from django.test import TestCase
import binascii
from asapp.b64url_enhancement import check_base64, b64url_decode_str, b64url_encode_str

# Generated with the help of ChatGPT 3.5,
# https://chat.openai.com/share/f7a9c685-b0c3-4455-ab18-312d4b5ac1c2

class CheckBase64TestCase(TestCase):
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


class B64urlDecodeStr(TestCase):
    def test_valid_decode(self):
        # Test valid base64 encoded string
        text = "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdC4"
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", b64url_decode_str(text))

    def test_invalid_unicode_base64(self):
        # Test invalid base64 encoded string
        text = "This is not a valid base64 encoded string"
        with self.assertRaises(UnicodeDecodeError):
            b64url_decode_str(text)
    
    def test_invalid_buffer_base64(self):
        # Test invalid base64 encoded string
        text = "invalid_base64_string"
        with self.assertRaises(binascii.Error):
            b64url_decode_str(text)

    def test_empty_string(self):
        # Test empty string
        text = ""
        self.assertEqual("", b64url_decode_str(text))

    def test_nonstring_decode(self):
        text = 12345
        with self.assertRaises(TypeError):
            b64url_decode_str(text)

    def test_unicode_decode(self):
        # Test non-string input
        text = "5L2g5aW977yM8J-YiiAgJiDhk4fhlpXhkqXhkoMg4ZaD4ZWG4ZO04ZCF4ZSq4ZaF "
        self.assertEqual('你好，😊  & ᓇᖕᒥᒃ ᖃᕆᓴᐅᔪᖅ', b64url_decode_str(text))

    def test_control_decode(self):
        text = 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8'
        self.assertEqual("\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F", b64url_decode_str(text))


class B64urlEncodeStr(TestCase):
    def test_valid_encode(self):
        # Test valid base64 encoded string
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.assertEqual("TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdC4", b64url_encode_str(text))

    def test_empty_string(self):
        # Test empty string
        text = ""
        self.assertEqual("", b64url_encode_str(text))

    def test_nonstring_decode(self):
        text = 12345
        with self.assertRaises(TypeError):
            b64url_encode_str(text)

    def test_unicode_decode(self):
        # Test non-string input
        text = '你好，😊  & ᓇᖕᒥᒃ ᖃᕆᓴᐅᔪᖅ'
        self.assertEqual('5L2g5aW977yM8J-YiiAgJiDhk4fhlpXhkqXhkoMg4ZaD4ZWG4ZO04ZCF4ZSq4ZaF', b64url_encode_str(text))

    def test_control_decode(self):
        text = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F"
        self.assertEqual('AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8', b64url_encode_str(text))
    