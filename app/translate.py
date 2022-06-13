import json
import requests
from flask import current_app
from flask_babel import _


def get_headers():
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(current_app.config['MS_TRANSLATOR_KEY'])
    }

    return headers

def translate(text, source_language, dest_language):

    headers = get_headers()

    body_get_translate_text = {
        "sourceLanguageCode": source_language,
        "targetLanguageCode": dest_language,
        "texts": [text],
        "folderId": current_app.config['MS_FOLDER_ID']
    }

    post_get_translate_text = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                            json=body_get_translate_text,
                                            headers=headers)

    if post_get_translate_text.status_code != 200:
        return _('Error: the translation service failed.')
    return post_get_translate_text.json()["translations"][0]["text"]

def get_language(text):

    headers = get_headers()

    body_get_language = {
        "folderId": current_app.config['MS_FOLDER_ID'],
        "text": text
    }

    post_get_language = requests.post('https://translate.api.cloud.yandex.net/translate/v2/detect',
                                      json=body_get_language,
                                      headers=headers)

    if post_get_language.status_code != 200:
        return _('Error: the translation service failed.')
    return post_get_language.json()["languageCode"]