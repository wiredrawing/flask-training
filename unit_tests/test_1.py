import unittest
from unittest.mock import MagicMock, patch

from routes.CreateUserForm import check_email, duplicate_email


class TestCreateUserForm(unittest.TestCase):
    def test_check_email_success(self):
        form_mock = MagicMock();
        field_mock = MagicMock();
        field_mock.data = "test@gmail.com";
        self.assertEqual(check_email(form_mock, field_mock), None)

    def test_check_email_failed(self):
        form_mock = MagicMock();
        field_mock = MagicMock();
        field_mock.data = "test@gmail";
        with self.assertRaises(Exception):
            check_email(form_mock, field_mock)

    def test_duplicate_email_success(self):

        form_mock = MagicMock();
        field_mock = MagicMock(data="test@gmail.com")
        self.assertEqual(duplicate_email(form_mock, field_mock), None)


if __name__ == "__main__":
    unittest.main()
