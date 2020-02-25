from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

drinks = pandas.read_excel('wine.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')

categorized_drinks = {}
for drink in drinks:
    if drink['Категория'] not in categorized_drinks:
        categorized_drinks[drink['Категория']] = []
    categorized_drinks[drink['Категория']].append(drink)

year_of_foundation = 1920
age = datetime.now().year - year_of_foundation

rendered_page = template.render(
    age=age,
    categorized_drinks=categorized_drinks,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
