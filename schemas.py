from random import randint, seed

def set_value(schema: dict[str:str], model: dict, name: str, value: any):
    param = schema[name]
    path = param["path"].split("/")
    level = model
    for p in path[:-1]:
        level = level[p]
    
    match param["type"]:
        case "str":
            value = str(value)
        case "int":
            value = int(value)
        case "bool":
            value = bool(value)
        case "float":
            value = float(value)
    level[path[-1]] = value

def set_seed(schema: dict[str:str], model: dict):
    seed()
    for i in range(1000):
        if not f"rseed{i}" in schema.keys():
            print(f"rseed{i}", schema.keys())
            break
        set_value(schema, model, f"rseed{i}", randint(0, 10 ** 16))