import nltk
import numpy as np 
import random
import string
import quandl
import json
from googlesearch import search
import sys
from fotos import detectar_manos
import requests
import recognize_video as rv
from TTS import iTTS



quandl.ApiConfig.api_key = "K6Eu4_MkhWsvPqzJQWRV"

# import sklearn

f = open('chatbot.txt','r',errors = 'ignore')

raw = f.read()

raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
	return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
	return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("salve", "eai", "oi", "ola", "beleza?","fala",)
GREETING_RESPONSES = ["fala tu", "oi",  "tranquilo?", "e ai fake", "to felizão que voce ta falando comigo", "oi razao dos meus pensamentos impuros", "salve quebrada"]
GET_FACE_DETECTION = ['detectar', 'quem sou eu?', "qual teu nome pai?"]
GET_WEATHER_INPUTS = ('clima', 'tempo', 'temperatura', 'vento', 'chuva', 'chover', 'sol', 'humidade')



def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def show_weather():
    api_key = "5996bb7475362a7cfaa36fae8a25935e"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + 'dublin'
    response = requests.get(complete_url) 

    resp = response.json() 
    if resp["cod"] != "404": 
        meteorologia = resp["main"] 
        current_temperature = meteorologia["temp"] 
    
        current_pressure = meteorologia["pressure"] 
    
        current_humidiy = meteorologia["humidity"] 
    
        z = resp["weather"] 

        weather_description = z[0]["description"] 
        print(" temperatura em kelvin = " +
                        str(current_temperature) + 
            "\n pressao em pascal = " +
                        str(current_pressure) +
            "\n humidade em porcentagem = " +
                        str(current_humidiy) +
            "\n descricao = " +
                        str(weather_description)) 
    else: 
        print(" City Not Found ") 


GETSTOCK_INPUTS = ('acoes', 'bolsa', 'valores', )
TICKER_INPUTS =  set()
with open('sp500tickers.txt', 'r') as f:
    for ticker in f.readlines():
        TICKER_INPUTS.add(ticker)
GETSTOCK_RESPONSES = (' os valores das ações da {0}: {1}\n', 'o historico de ações da {0} : {1}\n')

def stock_show(sentence):
    response = ''
    for word in sentence.split():
        if (word.upper()+'\n') in TICKER_INPUTS:
            # quandl_data = quandl.get_table('ZACKS/FR', ticker='{}'.format(word))
            quandl_data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'close'] }, ticker = ['{}'.format(word),], date = { 'gte': '2018-01-01', 'lte': '2018-04-31' })
            response = random.choice(GETSTOCK_RESPONSES).format(word, quandl_data)
        else:
            quandl_data = quandl.get("FRED/GDP", start_date="2017-12-31", end_date="2019-01-31")
            response = random.choice(GETSTOCK_RESPONSES).format("FRED/GDP", quandl_data)
    return response

def get_stock(sentence):
    for word in sentence.split():
        if word.lower() in GETSTOCK_INPUTS:
            return stock_show(sentence)

def get_detection(sentence):
    for word in sentence.split():
        if word.lower() in GET_FACE_DETECTION:
            detectar_manos()

def get_weather(sentence):
    for word in sentence.split():
        if word.lower() in GET_WEATHER_INPUTS:
            show_weather()

                

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

lista_nao_entendi = ["foi mal, não entendo o que voce ta querendo me falar.", "mano que? o que voce esta falando ", "repete ai, não ta fazendo sentido"]


def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)

    # TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+random.choice(lista_nao_entendi)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
iTTS(" E ai fake, meu nome é Insperina. Como posso te ajudar?. Se quiser sair, digite flw!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='flw'):
        if(user_response=='obrigado' or user_response=='vlw' ):
            flag=False
            iTTS(" Relaxa, tamo aqui para isso")
        else:
            if(greeting(user_response)!=None):
                iTTS( greeting(user_response))
            elif(get_stock(user_response)!=None):
                print( get_stock(user_response))
            elif(get_detection(user_response)!=None):
                print("Insperina: ")
                get_detection()
            elif(get_weather(user_response)!= None):
                print("ROBO: ")
                get_weather(user_response)
            else:
                print("Insperina: ",end="")
                iTTS(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        iTTS(" Falou! se cuida..")







