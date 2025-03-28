"""
Stock Upgrade Notifier Script
Author: Ed Guillen
Date: March 25, 2025
Description: This script fetches daily stock grade changes from a financial API 
             and sends a scheduled email notification with the results. Eventually 
             this script will send other types of notifications.
"""

import requests
import schedule
import time
import smtplib
import os
import json
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
API_KEY = os.environ["FMP_API_KEY"]
EMAIL_SENDER = os.environ["EMAIL"]
EMAIL_RECEIVER = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def fetch_stock_grade_changes():
    url = f"https://financialmodelingprep.com/stable/grades-latest-news?apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=3))
            grade_changes = [item for item in data if item.get('newGrade') == item.get('previousGrade')]
            
            if grade_changes:
                message = "Stock Grade Changes Today:\n\n"
                for stock in grade_changes:
                    message += f"{stock['symbol']} - {stock['gradingCompany']} upgraded from {stock['previousGrade']} to {stock['rating']}\n"
                    
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
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("Email sent successfully.")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

# Uncomment the below to test on the fly
#fetch_stock_grade_changes()

# Schedule the task at 6:15 AM PDT before the market open
schedule.every().day.at("06:15").do(fetch_stock_grade_changes)

print("Scheduler started. Running daily at 6:15 AM PDT.")
while True:
    schedule.run_pending()
    time.sleep(60)
    
