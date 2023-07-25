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
    def __init__(self, subject):
        self.subject = subject
        self.contents = []
        self.attachments = []


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

        mail = Mail(subject)
        for part in message.walk():
            if part.get_filename() is not None:
                mail.attachments.append(part)
            else:
                mail.contents.append(part)
        return mail

    def get_emails(self):
        mails = []
        for message_id in self._get_email_ids():
            _, msg = self.imap_server.fetch(message_id, '(RFC822)')
            mails.append(self._parse_email(msg[0][1], ))
        return mails


class Filter:
    def __init__(self, pattern, search_in_content, search_in_attachment_name):
        self.pattern = r"{}".format(pattern)
        self.search_in_content = search_in_content
        self.search_in_attachment_name = search_in_attachment_name
        self._is_mail_ok = False
        self.email = None

    def _search_in_content(self, part):
        return True if re.search(self.pattern, part.as_string(), re.IGNORECASE) else False

    def _search_in_attachment_name(self, part):
        return part.get_filename() is not None and re.match(self.pattern, part.get_filename(), re.IGNORECASE)

    def check(self):
        if self.email is None:
            raise ValueError("Email object is not set!")
        if self.search_in_content:
            for part in self.email.contents:
                self._is_mail_ok = self._search_in_content(part)

        if self.search_in_attachment_name:
            for attachment in self.email.attachments:
                self._is_mail_ok = self._search_in_attachment_name(attachment)
        return self._is_mail_ok


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
    filter = Filter(search, search_in_content, search_in_attachment_name)
    with open("config.yaml", "r") as file:
        credentials = yaml.safe_load(file)
        # pprint(credentials)
        for credential in credentials["mails"]:
            mailbox = MailBox(**credential)
            mailbox.connect()

            for email in mailbox.get_emails():
                filter.email = email
                if filter.check():
                    print(credential['login'], email.subject)
                    for attachment in email.attachments:
                        with open(os.path.join(uploads_to, attachment.get_filename()), "wb") as file:
                            file.write(attachment.get_payload(decode=True))


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
python main.py --search "Has(l||=C5=82)0" --search-in-content


"""

"""
Pamiętaj, że re.match() sprawdza tylko początek ciągu znaków. Jeśli chcesz znaleźć dopasowanie w 
dowolnym miejscu ciągu, możesz użyć funkcji re.search() zamiast niej.
"""
