import os, requests, uuid, json

# Не забудьте заменить своим ключом значение subscription_key!
subscription_key = 'b9300248783547b1ad5a3379b83b8e89'
location = 'global'


# Не забудьте заменить своим местоположением значение location! Наш маршрут Flask поставит два аргумента: text_input
# и language_output. При нажатии кнопки перевода текста в приложении Flask запрос Ajax возьмет эти значения из нашего
# веб-приложения и будет использовать их в запросе.
def get_translation(text_input, language_output):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # В теле можно передать несколько объектов.
    body = [{
        'text': text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
