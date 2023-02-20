import re
import deepl
import yaml

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

auth_key = data['auth_key']

def translate_html_text_content(html_string, language_code):
    # Use a regular expression to extract the text content from the HTML string
    text_content = re.sub(r'<[^<]+?>', '', html_string)

    # Translate the text content
    translated_text_content = translate_text(text_content, language_code)

    # Replace the text content in the HTML string with the translated text content
    translated_html = re.sub(r'([^<]+)?', translated_text_content, "")

    return translated_html


def translate_text(text, language_code):
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text=text, target_lang=language_code)
    translated_text = result.text
    return translated_text


def translate_html_file(path, article, language_code):
    new_path = '/Users/javier/IdeaProjects/vonfreiren.github.io/_spanish/'
    new_file= new_path+article

    filename = path+article
    with open(filename, 'r') as file:
        html_string = file.read()

    # Extract the metadata and main content
    metadata, main_content = html_string.split('---', 2)[1:]

    # Translate the main content
    translated_main_content = translate_html_text_content(main_content, language_code)

    # Combine the translated main content with the original metadata
    translated_html = '---\n' + metadata + '---\n' + translated_main_content

    with open(new_file, 'w') as file:
        file.write(translated_html)

language_code = "ES"
path = '/Users/javier/IdeaProjects/vonfreiren.github.io/_posts/'
file = '2023-02-14-top-blockchain-courses.md'

translate_html_file(path, file, language_code)
