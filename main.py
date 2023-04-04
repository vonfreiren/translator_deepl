import yaml

from main_calculations import translate_html_file

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

auth_key = data['auth_key']
path = data['path']
file = data['file']
language_code = data['language_code']
languages = data['languages']

for language_code in languages:

    translate_html_file(path, file, language_code)
