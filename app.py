from flask import Flask, render_template, request
import requests
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    
    # чтение данных из html формы
    original_text = request.form['text']
    target_language = request.form['language']

    # получение данных из .env файла
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # информируем, что мы хотим перевести, API
    # версии (3.0) и целевой язык
    path = '/translate?api-version=3.0'
    
    # добавляем целевой язык
    target_language_parameter = '&to=' + target_language
    
    # Создание полного URL-адреса
    constructed_url = endpoint + path + target_language_parameter

    # Настройка информации заголовка, которая включает
    # ключ подписки
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Создание тела запроса с текстом для перевода
    body = [{'text': original_text}]

    # отправляем запрос 
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)
    
    # получение ответа в виде JSON
    translator_response = translator_request.json()
    
    # получение перевода
    translated_text = translator_response[0]['translations'][0]['text']

    # вызов html шаблона, передача переведенного текста,
    # исходного текста и целевого языка в шаблон
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )