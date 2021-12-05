import pandas as pd
import matplotlib.pyplot as plt
import matplotlib 
from matplotlib import pyplot
from bs4 import BeautifulSoup
import requests
import numpy as np
from pandas import DataFrame
from pandas import Series
from Web.crawling import corona

def data():
    data = corona()
    city = {} #도시이름
    cityEn = {} # 도시영문
    today= {} #당일 지역 확진자
    total = {} #누적 지역확진자
    local = {} #지역발생 (해외유입 제외)
    foreign = {} #해외유입 발생
    #isolation = {} #현재 격리중
    dead = {}   #누적 사망자
    for number in range(len(data)):
        city[data[number]['gubun']] = data[number]['gubun']        
        cityEn[data[number]['gubun']] = data[number]['gubunEn']
        today[data[number]['gubun']] = data[number]['incDec']
        total[data[number]['gubun']] = data[number]['defCnt']       
        local[data[number]['gubun']] = data[number]['localOccCnt']
        foreign[data[number]['gubun']] = data[number]['overFlowCnt']
        #isolation[data[number]['gubun']] = data[number]['isolIngCnt']
        dead[data[number]['gubun']] = data[number]['deathCnt']

    # return {'city':city,'cityEn':cityEn,'today':today,'total':total,
    #                                    'local':local,'foreign':foreign,'isolation':isolation,'dead':dead}
    return {'city':city,'cityEn':cityEn,'today':today,'total':total,
                                       'local':local,'foreign':foreign, 'dead':dead}
def graph():
    plt.rc('font',family ='malgun gothic')
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=wAJqB4W%2F85JiEubCF29Bj%2Btb4zm2SDxoyM5gR7BkfCUTGq6YMBAcPVgmLw1wv0ccSg1T1E7XGd9jX9TlrqZebA%3D%3D&pageNo=1&numOfRows=20'
    
    result= requests.get(url, allow_redirects = False)
    soup = BeautifulSoup(result.text,"xml")
    items = soup.find_all("item")
    
    # df_col=['gubun','gubunEn','incDec','isolIngCnt',
    #         'localOccCnt','overFlowCnt','deathCnt','defCnt' ]
    df_col=['gubun','gubunEn','incDec',
            'localOccCnt','overFlowCnt','deathCnt','defCnt' ]
    list = []
    
    a=[]
    for item in items:
        name = item.find('gubun').string
        gubunEn = item.find('gubunEn').string
        incDec = item.find('incDec').string
        #isolIngCnt = item.find('isolIngCnt').string
        localOccCnt = item.find('localOccCnt').string
        overFlowCnt = item.find('overFlowCnt').string
        deathCnt = item.find('deathCnt').string
        defCnt = item.find('defCnt').string
    
        
        # a.append({'gubun':name,'gubunEn':gubunEn,'incDec':incDec,'isolIngCnt':isolIngCnt,
        #           'localOccCnt':localOccCnt,'overFlowCnt':overFlowCnt,'deathCnt':deathCnt,'defCnt':defCnt
        #               })
        a.append({'gubun':name,'gubunEn':gubunEn,'incDec':incDec,
                  'localOccCnt':localOccCnt,'overFlowCnt':overFlowCnt,'deathCnt':deathCnt,'defCnt':defCnt
                      })
    list.append(a)
    
    
    
    
    
    out_df = pd.DataFrame(a,columns=df_col)
    # out_df.columns=['지역이름','지역이름(영어)','확진자 수','격리중인 환자 수',
    #                 '내국인 확진자 수','외국인 확진자 수','사망자 수','누적 확진자 수'
    #         ]
    out_df.columns=['지역이름','지역이름(영어)','확진자 수',
                    '내국인 확진자 수','외국인 확진자 수','사망자 수','누적 확진자 수'
            ]
    
    out_df1= out_df.drop(index=[0])
    out_df1.to_csv("Project/Web/csv/today.csv")
    
    df1 = pd.read_csv("Project/Web/csv/today.csv")
    
    df1.sort_values(by=['누적 확진자 수'],ascending = True,inplace=True)
    df = df1.drop(index=[17])
    # df = df1
    #print(df)
    # print(df.head(3))
    # print(df.info())
    
    ys = df['누적 확진자 수'].to_list()
    xs = df['지역이름'].to_list()
    # df.plot(kind ='bar',y=['누적 확진자 수'],ylabel="누적 확진자숫자")
    plt.figure(figsize=(12,6))
    plt.ylabel('지역이름')
    plt.xlabel('누적 확진자 수')
    plt.barh(xs,ys)
    
    for i, v in enumerate(xs):
        str_val = '%d명'%ys[i]
        plt.text(ys[i],v, str_val,                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                 fontsize = 7, 
                 color='mediumblue',
                 horizontalalignment='left',  # horizontalalignment (left, center, right)
                 verticalalignment='center')    # verticalalignment (top, center, bottom)
    
    plt.savefig('Project/Web/static/graphs/korea.png', facecolor='#ffffff',edgecolor='blue'
                ,bbox_inches='tight', pad_inches=0.5)
    #facecolor= 외곽선 밖의 색 , edgecolor =외곽선 색,bbox_inches=‘tight’로 지정하면 여백을 최소화하고 그래프 영역만 이미지로 저장
    # pad_inches=bbox_inches=’tight’로 지정하면 pad_inches를 함께 사용해서 여백 (Padding)을 지정할 수 있습니다(0~1)
    
    from PIL import Image
     
    image = Image.open("Project/Web/static/graphs/korea.png")

    # plt.show()
    
    