import pdfkit
from jinja2 import Environment, FileSystemLoader
import json
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
env = Environment(loader=FileSystemLoader(__location__))
template = env.get_template('template.html')


def render_pdf() -> str:
    return


if __name__ == '__main__':
    with open(os.path.join(__location__, './test.json')) as fp:
        dummy = json.load(fp)
    pdfkit.from_string(template.render(dummy), './report.pdf')
    # 테스트 더미 데이터로 렌더링
