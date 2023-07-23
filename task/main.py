import imaplib
import email
import re
from email.header import decode_header
import yaml
from pprint import pprint
import os
import click

login = "stestl779@gmail.com"
password = "srdgglnrruqrmlfc"
server = "imap.gmail.com"


class Mail:
    def __init__(self, subject, contents):
        self.subject = subject
        self.contents = contents


class MailBox:
    def __init__(self, server, login, password):
        self.server = server
        self.login = login
        self.password = password
        self.imap_server = None

    def connect(self):
        self.imap_server = imaplib.IMAP4_SSL(host=self.server)
        self.imap_server.login(self.login, self.password)
        self.imap_server.select()

    def _get_email_ids(self):
        message_ids = self.imap_server.search(None, "All")
        return message_ids[1][0].split()

    def _parse_email(self, msg):
        message = email.message_from_bytes(msg)
        subject, subject_encoding = decode_header(message["Subject"])[0]
        if subject_encoding is not None:
            subject = subject.decode("utf-8")
        return Mail(
            subject, message.walk()
        )

    def get_emails(self):
        mails = []
        for message_id in self._get_email_ids():
            _, msg = self.imap_server.fetch(message_id, '(RFC822)')
            mails.append(self._parse_email(msg[0][1], ))
        return mails


@click.command()
@click.option('--uploads-to', type=click.Path(), default='attachments')
@click.option("--search", help="pattern to search in ...")
@click.option("--search-in-content", is_flag=True, help="Should I check content?")
@click.option("--search-in-attachment-name", is_flag=True, help="Should I check attachment?")
def main(uploads_to, search, search_in_content, search_in_attachment_name):
    print(search)
    print(search_in_attachment_name)
    print(search_in_content)
    os.makedirs(uploads_to, exist_ok=True)
    with open("config.yaml", "r") as file:
        credentials = yaml.safe_load(file)
        # pprint(credentials)
        for credential in credentials["mails"]:
            mailbox = MailBox(**credential)
            mailbox.connect()

            for email in mailbox.get_emails():
                is_mail_ok = False
                for part in email.contents:
                    if search_in_attachment_name:
                        search = r"{}".format(search)
                        if part.get_filename() is not None and re.match(search, part.get_filename(), re.IGNORECASE):
                            is_mail_ok = True
                            with open(os.path.join(uploads_to, part.get_filename()), "wb") as file:
                                file.write(part.get_payload(decode=True))
                    if search_in_content:
                        if re.search(search, part.as_string(), re.IGNORECASE):
                            if "Knedel" in part.as_string():
                                print(part.as_string())
                            is_mail_ok = True

                if is_mail_ok:
                    print(credential['login'], email.subject)


if __name__ == "__main__":
    main()

"""
python main.py --uploads-to=uploding
python main.py --search ABC --search-in-content
zadanie wyswietl tylko maile ktore maja jpg w zalaczniku:
python main.py --search .*\.jpg --search-in-attachment-name
python main.py --search .*\.jpg --search-in-attachment-name --uploads-to=photoJPG # bedzie wrzucał zdj do katalogu photoJPG
***
python main.py --search Has.*o --search-in-content # bo "ł" nie dzialalo!
python main.py --search "Has(l||=C5=82)0 --search-in-content

"""

"""
Pamiętaj, że re.match() sprawdza tylko początek ciągu znaków. Jeśli chcesz znaleźć dopasowanie w 
dowolnym miejscu ciągu, możesz użyć funkcji re.search() zamiast niej.
"""
