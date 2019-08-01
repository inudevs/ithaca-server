import json
import os.path
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

regs = [
    re.compile(r'\d{2}세기'),
    re.compile(r'\d{3}년'),
    re.compile(r'\d{4}년'),
    re.compile(r'\d{2}월'),
    re.compile(r'\d월'),
    re.compile(r'\d{2}일'),
    re.compile(r'\d일'),
]

if __name__ == '__main__':
    with open(os.path.join(__location__, './data.json')) as fp:
        data = json.load(fp)

    dels = []
    strips = []
    splits = []

    for keyword in data.keys():
        if len(keyword) == 1:
            dels.append(keyword)
            continue

        if any(reg.match(keyword) for reg in regs):
            dels.append(keyword)
            continue

        if any(char in keyword for char in ['”', '\n', '기원전']):
            dels.append(keyword)
            continue

        try:
            int(keyword)
            dels.append(keyword)
            continue
        except BaseException:
            pass

        if '(' in keyword:
            splits.append(keyword)
            continue

        if keyword != keyword.strip():
            strips.append(keyword)

    print('[*] dels:', *[repr(i) for i in dels])
    print('[*] strips:', *[repr(i) for i in strips])
    print('[*] splits:', *[repr(i) for i in splits])

    for de in dels:
        del data[de]

    for st in strips:
        tmp = data[st]
        data[st.strip()] = tmp
        del data[st]

    for sp in splits:
        new = sp.split('(')[0]
        data[new] = data[sp]
        del data[sp]

    with open(os.path.join(__location__, './data.json'), 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False, sort_keys=True)
        fp.write('\n')
