import pdfkit
from jinja2 import Environment, FileSystemLoader
import json
import os.path
import platform

if platform.system() not in ['Darwin', 'Windows']: # Cloud maybe...?
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(600,600))
    display.start()

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
env = Environment(loader=FileSystemLoader(__location__))
template = env.get_template('template.html')


def render_pdf(data, output_name) -> str:
    output_path = './uploads/pdf/{}.pdf'.format(output_name)
    pdfkit.from_string(template.render(data), output_path)
    return output_path


if __name__ == '__main__':
    with open(os.path.join(__location__, './test.json')) as fp:
        dummy = json.load(fp)
    render_pdf(dummy, 'test')
