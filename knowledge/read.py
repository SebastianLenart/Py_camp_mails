import yaml

with open("conf2.yaml", "r") as file:
    data_yaml = yaml.safe_load_all(file)
    print(data_yaml)
    print(next(data_yaml))


"""
with open("conf2.yaml", "r") as file:
    for line in file:
        print(line) # generator - 1 cykl to jedna linia zczytana
    # data = file.read()
    # print(data)

"""