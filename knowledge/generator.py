text = "Seba"
my_iter = iter(text)
print(my_iter)  # <str_iterator object at 0x0000025FE8D0CF70>
print(next(my_iter))

while True:
    try:
        next(my_iter)
    except StopIteration:
        break
       