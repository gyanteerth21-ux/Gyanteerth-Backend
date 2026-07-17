import asyncio
import logging
import os
import unittest
from unittest import mock
import aiosmtplib

# Set test environment variables BEFORE importing Emailservice
os.environ["SMTP_HOST"] = "email-smtp.ap-south-1.amazonaws.com"
os.environ["SMTP_PORT"] = "587"
os.environ["SMTP_USERNAME"] = "test-ses-smtp-username"
os.environ["SMTP_PASSWORD"] = "test-ses-smtp-password"
os.environ["EMAIL_FROM"] = "admin@gyanteerthlearning.com"

# Import Emailservice after setting environment variables
from Backend.utils.Emailservice import send_email, validate_email_config

class TestEmailService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Backup environment
        self.original_env = dict(os.environ)
        
        # Setup clean test logger
        self.logger = logging.getLogger("email_service")
        self.log_handler = TestLogHandler()
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)
        
        # Reset state
        from Backend.utils import Emailservice
        Emailservice._last_send_time = 0.0

    def tearDown(self):
        # Restore environment variables
        os.environ.clear()
        os.environ.update(self.original_env)
        
        # Clean up logger
        self.logger.removeHandler(self.log_handler)

    @mock.patch("aiosmtplib.send", new_callable=mock.AsyncMock)
    async def test_successful_email_sending(self, mock_send):
        # Call send_email
        await send_email(
            to_email="recipient@example.com",
            subject="Test Subject",
            body="<h1>Hello World</h1>"
        )
        
        # 1. Verify aiosmtplib.send was called once
        mock_send.assert_called_once()
        
        # Get the call arguments
        called_args, called_kwargs = mock_send.call_args
        
        # Extract sent message and connection parameters
        message = called_args[0]
        hostname = called_kwargs.get("hostname")
        port = called_kwargs.get("port")
        start_tls = called_kwargs.get("start_tls")
        username = called_kwargs.get("username")
        password = called_kwargs.get("password")
        
        # 2. Verify Correct From address matches EMAIL_FROM
        self.assertEqual(message["From"], "admin@gyanteerthlearning.com")
        
        # 3. Verify Correct recipient matches to_email
        self.assertEqual(message["To"], "recipient@example.com")
        
        # 4. Verify Correct subject matches subject
        self.assertEqual(message["Subject"], "Test Subject")
        
        # 5. Verify HTML body is included
        body_parts = [part.get_content().strip() for part in message.iter_parts()]
        self.assertIn("<h1>Hello World</h1>", body_parts)
        
        # 6. Verify Plain-text fallback is included
        # The main content is plain text if we use add_alternative, let's verify
        main_payload = message.get_payload()
        if isinstance(main_payload, list):
            plain_text_part = main_payload[0].get_content()
        else:
            plain_text_part = message.get_content()
        self.assertEqual(plain_text_part.strip(), "Your email client does not support HTML.")
        
        # 7. Verify SES SMTP hostname is used
        self.assertEqual(hostname, "email-smtp.ap-south-1.amazonaws.com")
        
        # 8. Verify Port 587 is used
        self.assertEqual(port, 587)
        
        # 9. Verify STARTTLS is enabled
        self.assertTrue(start_tls)
        
        # 10. Verify SMTP_USERNAME is used for authentication
        self.assertEqual(username, "test-ses-smtp-username")
        
        # 11. Verify SMTP_PASSWORD is used for authentication
        self.assertEqual(password, "test-ses-smtp-password")
        
        # 12. Verify EMAIL_FROM is NOT incorrectly used as SMTP_USERNAME
        self.assertNotEqual(username, "admin@gyanteerthlearning.com")
        
        # 13. Verify Sensitive credentials are never logged
        for record in self.log_handler.records:
            log_msg = record.getMessage()
            self.assertNotIn("test-ses-smtp-password", log_msg)
            # Ensure SMTP_USERNAME isn't logged either
            self.assertNotIn("test-ses-smtp-username", log_msg)

    @mock.patch("aiosmtplib.send", new_callable=mock.AsyncMock)
    async def test_validation_error_on_missing_config(self, mock_send):
        # Remove a required environment variable
        del os.environ["SMTP_HOST"]
        
        # Force re-validation
        from Backend.utils import Emailservice
        Emailservice._config_validated = False
        
        # We expect a ValueError
        with self.assertRaises(ValueError) as context:
            await send_email(
                to_email="recipient@example.com",
                subject="Test Subject",
                body="<h1>Hello World</h1>"
            )
            
        self.assertIn("SMTP_HOST", str(context.exception))
        # Ensure password isn't exposed in error
        self.assertNotIn("test-ses-smtp-password", str(context.exception))
        
        # Verify no send was attempted
        mock_send.assert_not_called()

    @mock.patch("aiosmtplib.send")
    async def test_retry_on_temporary_smtp_error(self, mock_send):
        # Mock behavior: raise temporary error twice, then succeed
        temp_exception = aiosmtplib.SMTPResponseException(451, "Requested action aborted: local error in processing")
        mock_send.side_effect = [temp_exception, temp_exception, None]
        
        # Patch asyncio.sleep to avoid waiting during test
        with mock.patch("asyncio.sleep", new_callable=mock.AsyncMock) as mock_sleep:
            await send_email(
                to_email="recipient@example.com",
                subject="Test Subject",
                body="<h1>Hello World</h1>"
            )
            
            # Verify send was called 3 times (1 initial + 2 retries)
            self.assertEqual(mock_send.call_count, 3)
            # Verify sleep was called twice with exponential backoff (2.0s, 4.0s)
            backoff_sleep_calls = [call[0][0] for call in mock_sleep.call_args_list if call[0][0] in (2.0, 4.0)]
            self.assertEqual(backoff_sleep_calls, [2.0, 4.0])

    @mock.patch("aiosmtplib.send")
    async def test_permanent_smtp_error_fails_immediately(self, mock_send):
        # Mock behavior: raise permanent 5xx error
        perm_exception = aiosmtplib.SMTPResponseException(554, "Message rejected: Email address is not verified")
        mock_send.side_effect = perm_exception
        
        with mock.patch("asyncio.sleep", new_callable=mock.AsyncMock) as mock_sleep:
            with self.assertRaises(aiosmtplib.SMTPResponseException):
                await send_email(
                    to_email="recipient@example.com",
                    subject="Test Subject",
                    body="<h1>Hello World</h1>"
                )
                
            # Verify send was called exactly once and failed immediately (no retries)
            self.assertEqual(mock_send.call_count, 1)
            mock_sleep.assert_not_called()

    @mock.patch("aiosmtplib.send")
    async def test_max_retries_reached(self, mock_send):
        # Mock behavior: raise temporary error indefinitely
        temp_exception = aiosmtplib.SMTPResponseException(421, "Service unavailable, closing transmission channel")
        mock_send.side_effect = temp_exception
        
        with mock.patch("asyncio.sleep", new_callable=mock.AsyncMock) as mock_sleep:
            with self.assertRaises(aiosmtplib.SMTPResponseException):
                await send_email(
                    to_email="recipient@example.com",
                    subject="Test Subject",
                    body="<h1>Hello World</h1>"
                )
                
            # Verify send was called 3 times (max_attempts)
            self.assertEqual(mock_send.call_count, 3)
            backoff_sleep_calls = [call[0][0] for call in mock_sleep.call_args_list if call[0][0] in (2.0, 4.0)]
            self.assertEqual(backoff_sleep_calls, [2.0, 4.0])


class TestLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)
