import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, ".")
from bull_signal_bot import fetch_stock_grade_changes, send_email


class TestBullSignalBot(unittest.TestCase):
    
    @patch("bull_signal_bot.requests.get")  # Mock API requests
    @patch("bull_signal_bot.send_email")    # Mock email function
    def test_fetch_stock_grade_changes_success(self, mock_send_email, mock_requests_get):
        """Test fetch_stock_grade_changes with a successful API response."""

        # Simulated API response
        mock_response_data = [
            {"symbol": "AAPL", "gradingCompany": "Goldman Sachs", "previousGrade": "Hold", "newGrade": "Buy"},
            {"symbol": "GOOG", "gradingCompany": "Morgan Stanley", "previousGrade": "Sell", "newGrade": "Hold"}
        ]
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = mock_response_data
        
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            fetch_stock_grade_changes()
        
        # Ensure email was sent
        mock_send_email.assert_called_once_with(
            "Daily Stock Grade Changes",
            "Stock Grade Changes Today:\n\nAAPL - Goldman Sachs upgraded from Hold to Buy\nGOOG - Morgan Stanley upgraded from Sell to Hold\n"
        )
        
        # Ensure correct content is written to file
        mock_file().write.assert_called_once_with(
            "Stock Grade Changes Today:\n\nAAPL - Goldman Sachs upgraded from Hold to Buy\nGOOG - Morgan Stanley upgraded from Sell to Hold\n"
        )
        
    @patch("bull_signal_bot.requests.get")  # Mock API requests
    @patch("bull_signal_bot.send_email")    # Mock email function
    def test_fetch_stock_grade_changes_empty(self, mock_send_email, mock_requests_get):
        """Test fetch_stock_grade_changes with a successful API response."""

        # Simulated API response
        mock_response_data = []
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = mock_response_data
        
        with patch("builtins.print") as mock_print:
            fetch_stock_grade_changes()
            
        mock_print.assert_any_call("No stock grade changes today.")
        
    @patch("bull_signal_bot.requests.get")
    def test_fetch_stock_grade_changes_api_failure(self, mock_requests_get):
        """Test API failure handling in fetch_stock_grade_changes."""
        
        # Ensure the mocked response has a real integer status_code
        mock_requests_get.return_value.status_code = 500
        mock_requests_get.return_value.json.return_value = {}

        with patch("builtins.print") as mock_print:
            fetch_stock_grade_changes()
        
        # Check the exact expected output
        mock_print.assert_any_call("Failed to retrieve stock grade changes. Status Code: 500")
        
    @patch("bull_signal_bot.requests.get", side_effect=Exception("Connection timed out"))
    def test_fetch_stock_grade_changes_timeout(self, mock_requests_get):
        """Test handling of a timeout during the API request."""
        with patch("builtins.print") as mock_print:
            fetch_stock_grade_changes()
        mock_print.assert_any_call("Error fetching stock grade changes: Connection timed out")

    @patch("bull_signal_bot.smtplib.SMTP_SSL")
    def test_send_email_success(self, mock_smtp):
        """Test sending an email successfully."""
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        send_email("Test Subject", "Test Body")
        
        mock_server.login.assert_called_once_with(os.environ["EMAIL"], os.environ["EMAIL_PASSWORD"])
        mock_server.send_message.assert_called_once()
    
    @patch("bull_signal_bot.smtplib.SMTP_SSL")
    def test_send_email_failure(self, mock_smtp):
        """Test handling failure when sending an email."""
        
        mock_smtp.side_effect = Exception("SMTP connection error")
        
        with patch("builtins.print") as mock_print:
            send_email("Test Subject", "Test Body")
            
        mock_print.assert_any_call("Failed to send email: SMTP connection error")
        
        
if __name__ == "__main__":
    unittest.main()
