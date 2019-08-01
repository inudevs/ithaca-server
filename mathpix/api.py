import sys
import base64
import requests
import json
import configparser
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = configparser.ConfigParser()
config.read(os.path.join(__location__, '../config.ini'))
app_id = config['MATHPIX']['app_id']
app_key = config['MATHPIX']['app_key']


def encode_image(filepath):
    with open(filepath, 'rb') as fp:
        image_uri = 'data:image/jpg;base64,{}'.format(
            base64.b64encode(fp.read()))
    return image_uri


def image_to_math(image_uri):
    r = requests.post('https://api.mathpix.com/v3/latex',
                      data=json.dumps({
                          'src': image_uri,
                          'formats': ['text', 'latex_normal', 'latex_styled']
                      }),
                      headers={
                          'app_id': app_id,
                          'app_key': app_key,
                          'Content-type': 'application/json'
                      })
    print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))


if __name__ == '__main__':
    image_uri = encode_image('./test.png')
    image_to_math(image_uri)
