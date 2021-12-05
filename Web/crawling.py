import requests
import xmltodict
import time

def corona():
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=wAJqB4W%2F85JiEubCF29Bj%2Btb4zm2SDxoyM5gR7BkfCUTGq6YMBAcPVgmLw1wv0ccSg1T1E7XGd9jX9TlrqZebA%3D%3D&pageNo=1&numOfRows=20'
    req = requests.get(url).content
    xmlObject = xmltodict.parse(req)    
    
    allData = xmlObject['response']['body']['items']['item']
   
    return allData