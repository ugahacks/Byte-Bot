import imaplib
import email
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

#Enum for the types of emails that can be recieved
class EmailType:
    EMAIL = 0
    ERROR = 1
    TEXT = 2
    UNDEFINED = 3


def get_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(EMAIL, PASSWORD)
    mail.select('INBOX')
    status, data = mail.search(None, 'UNSEEN')
    mail_list = []
    for mail_id in data[0].split():
        result, email_data = mail.fetch(mail_id, '(RFC822)')
        raw_email_as_string = email_data[0][1].decode('UTF-8')
        email_msg = email.message_from_string(raw_email_as_string)

        subject = str(email.header.make_header(email.header.decode_header(email_msg['Subject'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_msg['To'])))
        email_from = str(email.header.make_header(email.header.decode_header(email_msg['From'])))

        if 'New text message from' in subject:
            # If this is a text message, parse the body. Otherwise, ignore it.
            if email_msg.is_multipart():
                payload = email_msg.get_payload()[0]
                payload = str(payload)
                start_index = payload.find('<https://voice.google.com>')
                end_index = payload.find('To respond to this text message')

                # Depending on the type of verification code, the end_index text changes :(
                if end_index < 0:
                    end_index = payload.find('YOUR ACCOUNT <https://voice.google.com>')

                if start_index == -1 or end_index == -1 or start_index > end_index:
                    email_body = 'An error occured while attempting to fetch the 2FA code.'
                else:
                    email_body = payload[start_index + 27:end_index]
            else:
                email_body = 'An error occured while attempting to fetch the 2FA code.'
            type = EmailType.TEXT

        elif 'ERROR:' in subject:
            if email_msg.is_multipart():
                payload = email_msg.get_payload()[0]
                payload = str(payload)
                start_index = payload.find('quoted-printable')
                end_index = payload.find('Python Executable')

                link = payload.split('To view this discussion on the web visit')[1]
                link = link.replace('=\n', '')

                email_body = payload[start_index:end_index] + '\n\n Click the following link to view the full error: ' + link

            type = EmailType.ERROR

        else:
            email_body = None
            type = EmailType.EMAIL

        mail_list.append({
            'subject': subject,
            'email_to': email_to,
            'email_from': email_from,
            'email_body': email_body,
            'type': type,
            })
    #Not sure if this is needed.
    mail.close()
    mail.logout()

    return mail_list
