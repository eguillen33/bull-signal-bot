"""
Stock Upgrade Notifier Script
Author: Eduardo Guillen
Date: March 25, 2025
Description: This script fetches daily stock upgrades from a financial API 
             and sends a scheduled email notification with the results. 
             Eventually this script will send other types of notifications.
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
API_KEY = os.environ["BENZINGA_API_KEY"]
EMAIL_SENDER = os.environ["EMAIL"]
EMAIL_RECEIVER = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def fetch_stock_upgrades():
    url = f"https://financialmodelingprep.com/stable/grades-latest-news?apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=3))
            upgrades = [item for item in data if item.get('newGrade') == item.get('previousGrade')]
            
            if upgrades:
                message = "Stock Upgrades Today:\n\n"
                for stock in upgrades:
                    message += f"{stock['ticker']} - {stock['firm']} upgraded to {stock['rating']}\n"
                    
                # Log to file
                log_file = f"stock_upgrades_{datetime.now().date()}.txt"
                with open(log_file, "w") as f:
                    f.write(message)
                    
                # Send email
                send_email("Daily Stock Upgrades", message)
                print(f"Upgrades found. Email sent. Logged to {log_file}")
            else:
                print("No stock upgrades today.")
        else:
            print(f"Failed to retrieve stock upgrades. Status Code: {response.status_code}")
    
    except Exception as e:
        print(f"Error fetching stock upgrades: {e}")
        
def send_email(subject, body):
    """Sends an email notification with stock upgrades."""
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
#fetch_stock_upgrades()

# Schedule the task at 6:15 AM PDT before the market open
schedule.every().day.at("06:15").do(fetch_stock_upgrades)

print("Scheduler started. Running daily at 6:15 AM PDT.")
while True:
    schedule.run_pending()
    time.sleep(60)
    
