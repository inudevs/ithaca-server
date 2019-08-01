import json
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def load_words():
    with open(os.path.join(__location__, './data.json'), 'r') as fp:
        data = json.load(fp)
    return data


keywords = load_words()


def search(context):
    res = []
    for word in keywords:
        if word in context:
            res.append((word, keywords[word]))
    res.sort(key=lambda k: k[1], reverse=True)
    return [i[0] for i in res]
