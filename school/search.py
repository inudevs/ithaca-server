import json
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def memoize(f):
    class memodict(dict):
        __slots__ = ()

        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return memodict().__getitem__


def load_words():
    with open(os.path.join(__location__, './data.json'), 'r') as fp:
        data = json.load(fp)
    words = {}
    for word in data['school']:
        words[word] = {}
    return words


words = load_words()


@memoize
def autocomplete(query):
    ell = len(query)
    return sorted([w for w in words if w[: ell] == query])


if __name__ == '__main__':
    print(autocomplete('한국'))
