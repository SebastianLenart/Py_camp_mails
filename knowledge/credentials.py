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











