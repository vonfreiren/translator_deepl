import yaml

from main import translate_html_file

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

auth_key = data['auth_key']
path = data['path']
file = data['file']
language_code = data['language_code']
languages = data['languages']
production = data['production']

for language_code in languages:
        """
    Translates the HTML content of the file specified by `path` and `file` to the language specified by `language_code`.
    
    Args:
        path (str): The path to the directory containing the file to be translated.
        file (str): The name of the file to be translated.
        language_code (str): The ISO 639-1 language code to translate the file to.
    
    Returns:
        None
    """
translate_html_file(path, file, language_code)
