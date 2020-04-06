import json


def save(di: dict, arg='w', path='save.json') -> None:
    with open(path, arg) as js:  # or 'w'
        js.write(json.dumps(di, indent=4) + ',\n')
