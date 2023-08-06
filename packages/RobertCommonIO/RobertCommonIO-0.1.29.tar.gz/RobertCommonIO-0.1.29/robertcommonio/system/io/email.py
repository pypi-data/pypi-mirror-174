from typing import NamedTuple

import smtplib
import email.mime.multipart
import email.mime.text
from email.utils import formatdate


class EmailConfig(NamedTuple):
    HOST: str
    PORT: int
    USER: str
    PSW: str
    FROM: str


class FileAccessor:

    def __init__(self, config: EmailConfig):
        self.config = config

    def send_email(self, mail_tos: str, mail_content: str, mail_title: str = ''):
        smtp_msg = email.mime.multipart.MIMEMultipart()
        smtp_msg['from'] = self.config.FROM
        smtp_msg['to'] = mail_tos
        smtp_msg['subject'] = mail_title
        smtp_msg['date'] = formatdate(localtime=True)
        smtp_msg.attach(email.mime.text.MIMEText(mail_content))

        smtp_handle = smtplib.SMTP()
        smtp_handle.connect(self.config.HOST, self.config.PORT)
        smtp_handle.starttls()
        smtp_handle.login(self.config.USER, self.config.PSW)
        smtp_handle.sendmail(self.config.FROM, mail_tos.split(';'), smtp_msg.as_string())
        smtp_handle.quit()
