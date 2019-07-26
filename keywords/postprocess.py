import json
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':
    with open(os.path.join(__location__, './data.json')) as fp:
        data = json.load(fp)

    dels = []
    strips = []

    for keyword in data.keys():
        if any(char in keyword for char in ['”', '\n', '기원전']):
            dels.append(keyword)
            continue

        if keyword != keyword.strip():
            strips.append(keyword)

    print('[*] dels:', *[repr(i) for i in dels])
    print('[*] strips:', *[repr(i) for i in strips])
