import imaplib
import email
from email.header import decode_header

login = "stestl779@gmail.com"
password = "srdgglnrruqrmlfc"
server = "imap.gmail.com"

imap_server = imaplib.IMAP4_SSL(host=server)
imap_server.login(login, password)
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
    for part in message.walk():
        print(part)



























