import re

# nie czaje tego totalnie

mail = "stestl779@gmail.com"
mail = "stestl779$gmail.com"  # zwroci None
out = re.match(r'[a-z0-9.]+@[a-z.]+', mail)
print(out)


def mail_validator(mail):
    out = re.match(r'[a-z0-9.]+@[a-z.]+', mail)
    out2 = re.search(r'[a-z0-9.]+@[a-z.]+', mail)
    if out:
        return True
    return False


print(mail_validator(mail))
