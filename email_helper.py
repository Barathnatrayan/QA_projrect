import base64
import json
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, Attachment, FileContent, FileName, FileType, \
    Disposition, Cc, Bcc

from helpers.constants import MIME_TYPE_MAP
from logger import get_logger

log = get_logger(__name__)


class EmailHelper:
    def __init__(self):
        self.client = SendGridAPIClient(self.__load_sendgrid_api_key())
        self.from_email = "barath_natrayan@yahoo.com"
        self.cc = ['barath_natrayan@yahoo.com']
        self.bcc_email = []
        self.reply_to = "barath_natrayan@yahoo.com"
        self.to_email = ['barathktn@gmail.com']
        self.message = Mail()

    @staticmethod
    def __load_sendgrid_api_key():
        with open(os.getenv("SendgridKey"), "r") as f:
            api_json = json.load(f)
        return base64.b64decode(api_json['api_key']).decode()

    def send_email(self, subject, html_content, file_info_list):
        try:
            to_emails = [To(email_id) for email_id in set(self.to_email)]
            cc_emails = [Cc(email_id) for email_id in set(self.cc)]
            bcc_emails = [Bcc(email_id) for email_id in set(self.bcc_email)]
            self.message = Mail(from_email=self.from_email, to_emails=to_emails,
                                subject=subject, html_content=html_content)
            self.message.add_cc(cc_emails)
            self.message.add_bcc(bcc_emails)
            self.message.reply_to = self.reply_to
            self.add_email_attachments(file_info_list)
            response = self.client.send(self.message)
            log.info("Response is {}".format(response.status_code))
            if response.status_code in [200, 201, 202]:
                log.info("Successfully sent mail")
        except Exception as e:
            log.error(f"Error occurred while sending email: Err {e} Body: {e}")

    def add_email_attachments(self, file_info_list):
        for file_info in file_info_list:
            file_name = file_info.file_name
            file_path = file_info.file_path
            file_type = file_info.file_type
            with open(file_path, 'rb') as f:
                data = f.read()
            file_encoded = base64.b64encode(data).decode()
            attachment = Attachment(FileContent(file_encoded), FileName(file_name),
                                    FileType(MIME_TYPE_MAP[file_type]), Disposition('attachment'))
            self.message.add_attachment(attachment)
