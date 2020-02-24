from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

wines = pandas.read_excel('wine.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')
print(wines)
white_wines = [wine for wine in wines if wine['Категория'] == 'Белые вина']
red_wines = [wine for wine in wines if wine['Категория'] == 'Красные вина']
drinks = [wine for wine in wines if wine['Категория'] == 'Напитки']

year_of_foundation = 1920
age = datetime.now().year - year_of_foundation

rendered_page = template.render(
    age=age,
    white_wines=white_wines,
    red_wines=red_wines,
    drinks=drinks
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
