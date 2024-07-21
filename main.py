import yaml
from main_calculations import translate_html_text_content
from main_calculations import translate_html_file

class Config:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    @property
    def auth_key(self):
        return self.data['auth_key']

    @property
    def path(self):
        return self.data['path']

    @property
    def file(self):
        return self.data['file']

    @property
    def language_code(self):
        return self.data['language_code']

    @property
    def languages(self):
        return self.data['languages']

config = Config('config.yaml')

for language_code in config.languages:
    translate_html_file(config.path, config.file, language_code)
