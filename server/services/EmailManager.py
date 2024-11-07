# IMPORTS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class EmailManager:
    """
    Handles email operations using Mailtrap for testing
    """
    def __init__(self, username: str, password: str, base_url: str):
        """
        Initialize EmailManager with Mailtrap credentials
        
        Args:
            username (str): Mailtrap username/API token
            password (str): Mailtrap password
            base_url (str): Base URL of your application
        """
        self.username = username
        self.password = password
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
        msg['From'] = "noreply@yourapp.com"
        msg['To'] = to_email
        msg['Subject'] = "Account Verification Request"

        verification_url = f"{self.base_url}/authenticate/verify/{verification_code}"
        
        body = f"""
        Hello {username},

        An administrator has created an account for you. To verify your account and set up your password, 
        please use the following verification code:

        {verification_code}

        You can enter this code at {self.base_url}/authenticate/verify/

        If you did not request this account, please ignore this email.

        Best regards,
        Your Application Team
        """

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.mailtrap.io', 2525)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")