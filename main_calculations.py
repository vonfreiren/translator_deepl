import re
import deepl
import yaml
from unidecode import unidecode

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

auth_key = data['auth_key']
path = data['path']
file = data['file']
language_code = data['language_code']

def select_destination_path(language_code):
    if language_code == 'EN':
        return data['destination_path']
    elif language_code == 'ES':
        return data['destination_path_es']
    elif language_code == 'FR':
        return data['destination_path_fr']
    elif language_code == 'DE':
        return data['destination_path_de']
    else:
        return data['destination_path']

def translate_html_text_content(html_string, language_code):
    # Use a regular expression to extract the text content from the HTML string
    #text_content = re.sub(r'<[^<]+?>', '', html_string)
    text_content = html_string

    # Translate the text content
    translated_text_content = translate_text(text_content, language_code)

    # Replace the text content in the HTML string with the translated text content
    translated_html = re.sub(r'([^<]+)?', translated_text_content, "")

    translated_html = translated_html.replace('<p>', "")
    translated_html = translated_html.replace('</p>', "")

    return translated_html


def translate_text(text, language_code):
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text=text, target_lang=language_code)
    translated_text = result.text
    return translated_text

def translate_metadata(metadata, language_code):
    values = ['description', 'title', 'subtitle']

    translator = deepl.Translator(auth_key)
    translated_metadata = metadata

    for value in values:
        pattern = r"%s: \"(.*?)\"" % value
        match = re.search(pattern, metadata)
        if match:
            text = match.group(1)
            result = translator.translate_text(text=text, target_lang=language_code)
            translated_metadata = translated_metadata.replace(text, result.text)
    match_lang= re.search(r"lang: (\w+)", metadata)
    if match_lang:
        lang = match_lang.group(1)
        old_lang = "lang: "+lang
        new_lang = "lang: "+language_code.lower()
        translated_metadata = translated_metadata.replace(old_lang, new_lang)

    return translated_metadata

"""
Initializes a DeepL translator with the provided authentication key.

Args:
    article (dict): The article to be translated.
    language_code (str): The target language code for the translation.

Returns:
    None
"""
def translate_article(article, language_code):
    translator = deepl.Translator(auth_key)
    pattern = r"(\d{4}-\d{2}-\d{2})"
    match = re.search(pattern, article)
    if match:
        date_value = match.group(1)
        title = article.split(date_value, 1)[1]
        title_parts = title.split('.')
        original_title = title_parts[0].replace('-', ' ')
        translated_title = translator.translate_text(text=original_title, target_lang=language_code).text
        translated_title = translated_title.replace(' ', '-')
        translated_title = unidecode(translated_title, 'utf-8')
        translated_title = translated_title.replace("'", '-')
        translated_title = translated_title.lower()
        new_article = f"{date_value}{translated_title}.{'.'.join(title_parts[1:])}"
    return new_article

def translate_html_file(path, article, language_code):

    destination_path = select_destination_path(language_code)

    translated_article = translate_article(article, language_code)
    new_file= destination_path+translated_article


    filename = path+article
    with open(filename, 'r') as file:
        html_string = file.read()

    # Extract the metadata and main content
    metadata, main_content = html_string.split('---', 2)[1:]
    translated_metadata = translate_metadata(metadata, language_code)
    # Translate the main content
    translated_main_content = translate_html_text_content(main_content, language_code)

    # Combine the translated main content with the original metadata
    translated_html = '---\n' + translated_metadata + '---\n' + translated_main_content

    with open(new_file, 'w') as file:
        file.write(translated_html)


translate_html_file(path, file, language_code)
