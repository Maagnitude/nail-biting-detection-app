import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pyautogui
import time


class Email():
    
    def __init__(self, username=None, password=None, receiver_email=None):
        self.smtp_server = "smtp.gmail.com"                  # Email server
        self.smtp_port = 587                                 # 587 for TLS - 465 for SSL
        self.smtp_username = username                        # Your email address
        self.smtp_password = password                        # Email password or App-specific password
        self.sender_email = username                         # Sender's email
        self.receiver_email = receiver_email                 # Receiver's email
        self.subject = "Nail Biting Detected!"               # Email subject
        self.n_screenshot = 0
        self.message = f"Nail biting detected at {time.strftime('%H:%M:%S')}!"
        
        
    def _create_email(self):
        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = self.subject
        msg.attach(MIMEText(self.message, "plain"))
        
        # Capture a screenshot
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        screenshot_path = f"{screenshots_dir}/screenshot{self.n_screenshot}.png"
        pyautogui.screenshot(screenshot_path)
        self.n_screenshot += 1
        print(f"Screenshot saved as '{screenshot_path}'")
        
        # Attach the screenshot to the email
        with open(screenshot_path, "rb") as screenshot_file:
            screenshot_attachment = MIMEApplication(screenshot_file.read(), Name=os.path.basename(screenshot_path))
            screenshot_attachment["Content-Disposition"] = f"attachment; filename={os.path.basename(screenshot_path)}"
            msg.attach(screenshot_attachment)
            print(f"Screenshot attached to email!")    
        return msg
        
        
    def send_email(self):
        msg = self._create_email() 
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()                                       # Start TLS encryption
            server.login(self.smtp_username, self.smtp_password)    # Login to the server
            print(f"Connected to {self.smtp_server} server!")
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print(f"Email sent successfully to {self.receiver_email}!")