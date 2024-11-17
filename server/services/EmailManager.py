# EmailManager.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

class EmailManager:
    """
    Handles email operations using Gmail SMTP
    """
    def __init__(self, gmail_user: str, gmail_password: str, base_url: str):
        """
        Initialize EmailManager with Gmail credentials
        
        Args:
            gmail_user (str): Gmail email address
            gmail_password (str): Gmail app password
            base_url (str): Base URL of your application
        """
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.base_url = base_url

    def send_verification_email(self, to_email: str, username: str, verification_code: str) -> None:
        """
        Send verification email with confirmation link
        
        Args:
            to_email (str): Recipient's email address
            username (str): Username of the new user
            verification_code (str): Verification code for the user
        """
        msg = MIMEMultipart()
        msg['From'] = self.gmail_user
        msg['To'] = to_email
        msg['Subject'] = "BCIT Account Verification"
        
        # Ensure we're using the React app URL
        verification_url = f"{self.base_url}/authenticate/verify/{verification_code}"
        
        body = f"""
        Hello {username},

        An administrator has created an account for you at BCIT Global Relations Office. 
        To verify your account, please click the link below:

        {verification_url}

        If you cannot click the link, copy and paste it into your browser.

        Note: If you did not request this account, please ignore this email.

        Best regards,
        BCIT Global Relations Office
        """
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.close()
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")