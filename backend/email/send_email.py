import base64
import logging
import os
import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from deta import Deta
from dotenv import load_dotenv

from frontend.utils.utils import get_img_with_href

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

DETA = Deta(os.getenv("DETA_KEY"))


class EmailService():

    @staticmethod
    def connect_db(db: str):
        return DETA.Base(db)

    @classmethod
    def get_subscription_list(cls) -> list:
        subscription_db = cls.connect_db('subscription_db')
        return [
            subscribed['key']
            for subscribed in subscription_db.fetch().items
            if subscribed['is_subscribed']
        ]

    @classmethod
    def get_item(cls, item_name: str) -> dict:
        item_db = cls.connect_db('items_db2')
        key = item_name.replace(' ', '_')
        return item_db.get(key=key)

    @staticmethod
    def get_image(catalog: str, name: str):
        return DETA.Drive('images_db').get(f"/{catalog}/{name}").read()

    # Function to send the email

    @classmethod
    def send_email(cls, recipient_email: str, item_dict: dict = None, subscription_event: str = None):
        sender_email: str = os.getenv('email_sender_name')
        msg = MIMEMultipart()
        if item_dict:
            image_data = cls.get_image(
                name=item_dict['image_name'], catalog=item_dict['catalog'])
            item_name = item_dict['name']
            item_description = item_dict['description']
            item_link = item_dict['affiliate_link']
            item_image_name = item_dict['image_name']
            item_viewed = item_dict['clicked'] + item_dict['f_clicked']
            dark_theme = {
                "background-color": "#0E1117",
                "secondary-background-color": "#262730",
                "text-color": "#FAFAFA"
            }
            light_theme = {
                "background-color": "#FFFFFF",
                "secondary-background-color": "#F0F2F6",
                "text-color": "#31333F"
            }

            theme = dark_theme

            cons = [f'<li>❌ {i}</li>' for i in item_dict['pros'].split('. ')]
            pros = [f'<li>✅ {i}</li>' for i in item_dict['cons'].split('. ')]
            # Create the email message
            subject = item_name

            # --- PATH SETTINGS ---
            current_dir = Path(
                __file__).parent if "__file__" in locals() else Path.cwd()
            email_body_file = current_dir / 'backend' / 'email' / 'email_body.html'

            # Read the HTML file
            with open(email_body_file, "r") as file:
                html_content = file.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            current_dir = Path(
                __file__).parent if "__file__" in locals() else Path.cwd()
            aibestgoods_logo_path = current_dir / 'assets' / 'logo.png'
            aibestgoods_logo = get_img_with_href(
                aibestgoods_logo_path, "AIBestGoods")

            html_content = html_content\
                .replace("AIBESTGOODS_ICON", aibestgoods_logo)\
                .replace("PRIMARY_COLOR", theme['background-color'])\
                .replace("SECONDARY_COLOR", theme['secondary-background-color'])\
                .replace("ITEM_NAME", item_name)\
                .replace("ITEM_LINK", item_link)\
                .replace("IMAGE_DATA", image_base64)\
                .replace("IMAGE_ALT", item_image_name)\
                .replace("ITEM_VIEWED", f'🔥 {item_viewed}')\
                .replace("ITEM_PROS", ''.join(pros))\
                .replace("ITEM_CONS", ''.join(cons))\
                .replace("ITEM_DESCRIPTION", item_description.split('. ')[0])

            msg.attach(MIMEText(html_content, 'html'))
        else:
            subject = subscription_event

        msg['From'] = formataddr(("AIBestGoods", f"{sender_email}"))
        msg['To'] = recipient_email
        msg['Subject'] = f'👉 {subject}'
        # msg.attach(image)

        # Setup the SMTP server
        smtp_server = 'smtp.titan.email'
        smtp_port = 587

        # Create a secure connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the sender's email account
        server.login(sender_email, os.getenv("email_password"))

        # Send the email
        server.sendmail(sender_email, recipient_email,
                        msg.as_string('email_password'))

        # Close the connection to the SMTP server
        server.quit()

        logging.info(f'Email sent successfully to {recipient_email}!')


if __name__ == '__main__':
    email_obj = EmailService()
    emails_to_send = email_obj.get_subscription_list()
    item_dict = email_obj.get_item("August_Home")

    for email in emails_to_send:
        if not item_dict['email_sent']:
            email_obj.send_email(recipient_email=email, item_dict=item_dict)

    # Schedule the email to be sent every day at a specific time
    # schedule.every().day.at("11:22").do(x)
    # schedule.every(1).minutes.do(x)

    # Continuously run the scheduler
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
