import imaplib
import email
from email.header import decode_header
from credentials import host, username, password

imap_server = imaplib.IMAP4_SSL(host=host)
imap_server.login(username, password)
imap_server.select("SPAM") # nazwa folderu
message_ids = imap_server.search(None, "ALL")
print(message_ids[1][0].split()) # zwraca IDs wiadomosci, ale w bajtach
for message_id in message_ids[1][0].split():
    tuple1, tuple2 = imap_server.fetch(message_id, "RFC822")
    print(tuple1) # OK
    print(tuple2[0][1]) # TEXT
    message = email.message_from_bytes(tuple2[0][1])
    print(message) # bardziej obrobiona wiadomosc bez krzakow
    print(decode_header(message["Subject"]))
    print(decode_header(message["From"]))
    subject, subject_encoding = decode_header(message["Subject"])[0]
    if subject_encoding is not None:
        subject = subject.decode("utf-8")
    email_from, from_encoding = decode_header(message["From"])[0]
    if from_encoding is not None:
        email_from = email_from.decode("utf-8")
    print("v2:", decode_header(message["Subject"]))
    print("v2:", decode_header(message["From"]))

    # zalaczniki - bloki, pobieranie plikow
    for chunk in message.walk():
        if chunk.get_filename() is not None:
            file = open(chunk.get_filename(), "wb")
            print(chunk.get_content_maintype(), chunk.get_filename())
            print(chunk.get_payload(decode=True)) # pobieranie zawartosci pliku
            # quit()












