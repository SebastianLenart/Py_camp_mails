import imaplib
import email
from email.header import decode_header
import yaml
from pprint import pprint
import os

login = "stestl779@gmail.com"
password = "srdgglnrruqrmlfc"
server = "imap.gmail.com"


os.makedirs('attachments/', exist_ok=True)
with open("config.yaml", "r") as file:
    credentials = yaml.safe_load(file)
    # pprint(credentials)
    for credential in credentials["mails"]:
        print(credential)

        imap_server = imaplib.IMAP4_SSL(host=credential['server'])
        imap_server.login(credential['login'], credential['password'])
        imap_server.select()
        message_ids = imap_server.search(None, "All")
        for message_id in message_ids[1][0].split():
            _, msg = imap_server.fetch(message_id, '(RFC822)')
            message = email.message_from_bytes(msg[0][1])
            subject, subject_encoding = decode_header(message["Subject"])[0]
            # print(message)
            # print(subject)
            if subject_encoding is not None:
                subject = subject.decode("utf-8")
            print(credential['login'], subject)

            for part in message.walk():
                if part.get_filename() is not None:
                    with open('attachments/' + part.get_filename(), "wb") as file:
                        file.write(part.get_payload(decode=True))
                        print("pobrano")
