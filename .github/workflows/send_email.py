import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"


#load environment variables from .env file
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

print("Looking for .env at:", envars)
print("Exists:", envars.exists())
print("EMAIL loaded:", os.getenv("EMAIL"))


#read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")






def send_email(subject, reciever_email, name, due_date, invoice_no, amount):
    #create the base text message   
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = formataddr(('Sejahtera Center.',f"{sender_email}")) 
    msg['To'] = reciever_email
    msg['BCC'] = sender_email

    msg.set_content(
        f"""\
        Dear {name},
        This is a reminder that your payment for invoice number {invoice_no} of amount ${amount} is due on {due_date}. Please make the payment at your earliest convenience.
        Thank you for your prompt attention to this matter.
        Best regards,
        Sejahtera Center.
        """
        )
    msg.add_alternative(
        f"""\
        <html>
        <body>
            <p>Dear {name},</p>
            <p>This is a reminder that your payment for invoice number <strong>{invoice_no}</strong> of amount <strong>${amount}</strong> is due on <strong>{due_date}</strong>. Please make the payment at your earliest convenience.</p>
            <p>Thank you for your prompt attention to this matter.</p>
            <p>Best regards,</p>
            <p>Sejahtera Center.</p>
        </body>
        </html>
    """,
        subtype='html'
    )

    #send the email
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, reciever_email, msg.as_string())
        

if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        reciever_email="kucai1519@gmail.com",
        name="John Doe",
        due_date="2026-7-31",
        invoice_no="INV-21-12-009",
        amount="100.00"
    )