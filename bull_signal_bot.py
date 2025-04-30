"""
Stock Upgrade Notifier Script
Author: Ed Guillen
Date: March 25, 2025
Description: This script fetches daily stock grade changes from a financial API
             and sends a scheduled email notification with the results. Eventually
             this script will send other types of notifications.
"""

import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
API_KEY: str = os.environ["FMP_API_KEY"]
EMAIL_SENDER: str = os.environ["EMAIL_SENDER"]
EMAIL_RECEIVERS: str = os.environ["EMAILS"]
EMAIL_PASSWORD: str = os.environ["EMAIL_PASSWORD"]


def fetch_stock_grade_changes():
    url = f"https://financialmodelingprep.com/stable/grades-latest-news?apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=(5))
        if response.status_code == 200:
            data = response.json()
            grade_changes = [item for item in data if item.get('newGrade') != item.get('previousGrade')]
            
            if grade_changes:
                message = "Stock Grade Changes Today:\n\n"
                for stock in grade_changes:
                    message += f"{stock['symbol']} - {stock['gradingCompany']} upgraded from {stock['previousGrade']} to {stock['newGrade']}\n"

                # Log to file
                log_file = f"stock_grade_changes_{datetime.now().date()}.txt"
                with open(log_file, "w") as f:
                    f.write(message)

                # Send email
                send_email("Daily Stock Grade Changes", message)
                print(f"Stock grade changes found. Email sent. Logged to {log_file}")
            else:
                print("No stock grade changes today.")
        else:
            print(f"Failed to retrieve stock grade changes. Status Code: {response.status_code}")
    
    except Exception as e:
        print(f"Error fetching stock grade changes: {e}")


def send_email(subject, body):
    """Sends an email notification with stock grade changes."""
    print("Sending Email to clients... ")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            
            for email_receiver in EMAIL_RECEIVERS.split(","):
                email_receiver = email_receiver.strip()
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = EMAIL_SENDER
                msg["To"] = email_receiver
                
                server.send_message(msg)
                print("Email sent to", email_receiver)

    except Exception as e:
        print(f"Failed to send email: {e}")


fetch_stock_grade_changes()
