from django.shortcuts import render
from Web.models import Members
from Web.models import Graph
from django.contrib.auth.models import User

from django.contrib import auth
from django.conf import settings
from bs4 import BeautifulSoup
import requests

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import os
import statsmodels.formula.api as smf
import seaborn as sns
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense 
from tensorflow.keras import optimizers
from keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score
import json
import Web.main1 as m1
from PIL import Image
from docutils.nodes import image

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# Create your views here.
def initFunc(request): 
    return render(request, 'init.html')

def main1Func(request):
    m1.graph()
    data = m1.data()
    return render(request, 'main1.html', data)

def main2Func(request):
    return render(request, 'main2.html')

def seoulFunc(request):
    return render(request, 'city.html')

def signupFunc(request): #회원가입 페이지로 이동
    return render(request, 'signup.html')

def insertFunc(request): #회원가입 기능
    birth = str(request.POST.get("yy")) + str(request.POST.get("mm")) + str(request.POST.get("dd"));
    #print(birth);
    if request.method == 'POST':
        try: #userid가 테이블에 있으면 등록 x
            Members.objects.get(userid = request.POST.get('userid')) #입력한 id를 가져와 검색
            return render(request, 'signup.html', {'msg':'이미 등록된 아이디 입니다.'})            
        except Exception as e: #userid가 없을 경우
            Members(
                userid = request.POST.get("userid"),
                passwd = request.POST.get("passwd"),
                username = request.POST.get("username"),
                birth = str(request.POST.get("yy")) + str(request.POST.get("mm")) + str(request.POST.get("dd")),
                gender = request.POST.get("gender")
                ).save() # 입력한 것들을 저장(insert) 회원 등록!
                
    return render(request, 'init.html') #회원가입 완료시 메인으로

def updateFunc(request):
    birth = str(request.POST.get("yy")) + str(request.POST.get("mm")) + str(request.POST.get("dd"));
    #print(birth);
    if request.method == 'POST':
        user = Members.objects.get(userid = request.session['userid'])
        print(user)
        user.passwd = request.POST.get("passwd")
        user.username = request.POST.get("username")
        user.birth = birth
        user.gender = request.POST.get("gender")
        user.save()
    return render(request, 'init.html')

def login(request): #로그인 페이지로 이동
    return render(request, 'login.html')

def loginFunc(request): #로그인
    if request.method == 'POST':
        try: # user 아이디와 패스워드가 정상적으로 입력될 경우
            user = Members.objects.get(userid = request.POST.get('userid'), passwd = request.POST.get('passwd')) #입력한 id를 가져와 검색
            # request.session['user'] = user
            request.session['username'] = user.username # 세션에 검색된 유저이름를 담기.
            request.session['userid'] = user.userid # 세션에 검색된 유저아이디를 담기.
            keep = request.POST.get('keep')
            print('keep : ', keep)
            if(keep == '1'): 
                print('로그인 유지')
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            else:
                print('로그인 미유지')
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

            return render(request, 'init.html') # 메인으로                     
        except Exception as e:  #로그인 실패시
            return render(request, 'login.html', {'msg':'아이디 패스워드가 일치하지 않습니다.'}) # 다시 로그인 페이지로 돌아감.

def logoutFunc(request): # 로그 아웃
    if request.session.get('username'): # 세션이 있을 경우
        print(request.session.get('username'))
        request.session.clear() # 세션을 삭제
    return render(request, 'init.html') # 메인으로

def mypageFunc(request):
    # if(request.GET.get('image') != None):
    #     image = request.GET.get('image')
    #     target = Graph.objects.get(image = image)
    #     target.delete()
    #     file_name = 'C:/work/psou/Project/Web/static/graphs/' + str(request.GET.get('image')) + '.png'
    #         print(file_name)
    #         if os.path.exists(file_name):
    #             print('exist')
    #             os.remove(file_name)
    #         else:
    #             print('nono')
    if(request.GET.get('delete') != None):
        delCheck = request.GET.get('delete')
        list = delCheck.split(',')
        for item in list:
            target = Graph.objects.get(image = item)
            target.delete()
            file_name = 'Project/Web/static/graphs/' + item + '.png'
            print(file_name)
            if os.path.exists(file_name):
                print('exist')
                os.remove(file_name)
            else:
                print('nono')
    graph = Graph.objects.filter(userid = request.session.get('userid')) #입력한 id를 가져와 검색
    data = {'userid' : request.session.get('userid'), 'username':request.session.get('username'), 'graph' : graph}

    return render(request, 'mypage.html', data) 

def lifestyleFunc(request):
    return render(request, 'lifestyle.html')

def checkFunc(request):
    return render(request, 'check.html')

# 시각화
def delgraph(): #그래프, plot 데이터 초기화
    file_name = 'Project/Web/static/graphs/analysis.png'
    if os.path.exists(file_name):
        print('파일 삭제 진행')
        os.remove(file_name)
    plt.clf() #시각화 데이터 초기화

# def graphFunc(request):
#     delgraph() # 초기화
#     file_name = 'Project/Web/static/graphs/hobbies.png'
#     plt.figure(figsize = (5, 4)) # 그래프 사이즈 조절
#     plt.plot() # 빈그래프 입력
#     fig = plt.gcf() # 그래프 변수에 저장
#     fig.savefig(file_name) # 파일로 저장
#     return render(request, 'main2.html')
#
# def graph2Func(request):
#     delgraph() #초기화
#
#     df = pd.read_csv("Project/Web/csv/코로나바이러스감염증-19_백신별_일일_접종현황_20211117(0시 기준)(수정).csv",
#                      thousands=',') # 접종인구수의 쉼표를 제거하고 정수화 하기 위해 thousands 옵션을 이용해 ,제거
#     #print(df)
#
#     df = df.loc[df['날짜'].isin(['2021-02-28','2021-03-31','2021-04-30','2021-05-31', '2021-06-30','2021-07-31', '2021-08-31','2021-09-30', '2021-10-31', '2021-11-16'])]
#     df = df.sort_values('날짜') # 날짜 컬럼대로 정렬
#     #print(df)
#     se1 = df['1차'].values # 1차 접종자 값
#     se2 = df['완료'].values # 2차 접종자(완료) 값
#     #print(se2)
#
#     plt.figure(figsize = (7, 5))
#     plt.plot(se1, 'rs-', label='1차접종')
#     plt.plot(se2, 'bo-', label='2차접종(완료)')
#     plt.xlabel('월별(말일 기준)')
#     plt.ylabel('접종인구(천만)')
#     plt.xlim([0, 9])
#     plt.ylim([0,51349116])
#     plt.xticks([0,1,2,3,4,5,6,7,8,9], ['2월', '3월', '4월','5월','6월','7월','8월','9월','10월','11월'])
#     plt.title('전국민 백신 접종 현황(누적)')
#     plt.legend()
#
#     fig = plt.gcf()
#     fig.savefig('Project/Web/static/graphs/hobbies.png')
#     return render(request, 'main2.html')
#
# def graph3Func(request):
#     delgraph() # 초기화
#     df = pd.read_csv("Project/Web/csv/선별진료소_20211113113900.csv")
#     #print(df['시도'].unique())
#     #print(df.groupby(['시도']).size()) 
#     #print(df.groupby(['시도']).size().sum()) 
#     #print(df[df['시도'] == '서울'].count()) 
#     #print(len(df[df['시도'] == '경기']))
#     x_pie = [len(df[df['시도'] == '강원']),len(df[df['시도'] == '경기']),len(df[df['시도'] == '경남']),len(df[df['시도'] == '경북'])
#              ,len(df[df['시도'] == '광주']),len(df[df['시도'] == '대구']),len(df[df['시도'] == '대전']),len(df[df['시도'] == '부산'])
#              ,len(df[df['시도'] == '세종']),len(df[df['시도'] == '서울']),len(df[df['시도'] == '울산']),len(df[df['시도'] == '인천'])
#              ,len(df[df['시도'] == '전남']),len(df[df['시도'] == '전북']),len(df[df['시도'] == '제주']),len(df[df['시도'] == '충남'])
#              ,len(df[df['시도'] == '충북'])] # 각 시도 별 선별진료소 갯수
#     labels = ['강원', '경기', '경남', '경북', '광주','대구','대전','부산','세종','서울','울산','인천','전남','전북','제주', '충남', '충북']
#     explode = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.08, 0.13, 0.1, 0.1, 0.1, 0.1, 0.1]
#     plt.figure(figsize = (6, 6))
#     plt.pie(x_pie, labels=labels,autopct='%.1f%%', counterclock=False, explode=explode) #autopct:소숫점 표기, explode:그래프 돌출 정도
#     plt.title('지역별 선별 진료소 비율 현황')
#     fig = plt.gcf()
#     fig.savefig('Project/Web/static/graphs/hobbies.png')
#     return render(request, 'main2.html')
#
# def graph4Func(request):
#     delgraph()
#     df = pd.read_csv("django_finalproject/proapp/급성호흡기감염증- 바이러스(전체).csv")
#     #print(df)
#     df2 = df[df['구분'] == '총합']
#     df3 = df2.iloc[:, 1:4].T.values
#     df3 = list(df3.flatten())
#     print(df3)
#     df = df.drop(0, axis=0)
#     print(df)
#
#     vid2019 = df['2019'].values
#     vid2020 = df['2020'].values
#     vid2021 = df['2021'].values
#
#     plt.figure(figsize = (8, 8))
#     plt.subplots_adjust(hspace=0.4) # 서브 플롯 간의 세로 간격 설정
#     plt.subplot(2,1,1)
#     plt.plot(vid2019, 'rs-', label='2019년')
#     plt.plot(vid2020, 'bo-', label='2020년')
#     plt.plot(vid2021, 'vg--', label='2021년')
#     plt.xlabel('바이러스 종류')
#     plt.ylabel('감염인구수(명)')
#     plt.xlim([0, 6])
#     plt.xticks([0,1,2,3,4,5], ['아데노', '사람보카', '파라인플루엔자','호흡기세포융합','리노','사람메타뉴모'])
#     plt.title('기존 호흡기 질환명/연도별 발병 현황')
#     plt.legend()
#
#     plt.subplot(2,1,2)
#     plt.bar((1,2,3), df3)
#     plt.xlabel("연도")
#     plt.xticks([1,2,3], ['2019', '2020', '2021'])
#     plt.ylabel("총 감염인구수(명)")
#     plt.title('기존 호흡기 질환 연도별 총 발생')
#
#     fig = plt.gcf()
#     fig.savefig('Project/Web/static/graphs/hobbies.png')
#     return render(request, 'main2.html')
#
# def graph5Func(request):
#     delgraph()
#     df = pd.read_csv("Project/Web/csv/1년_동안_가장_많이_참여한_여가활동(남성).csv")
#     df1 = df['취미항목'].values
#     df2 = df['2019'].values
#     df3 = df['2020'].values
#     print(df2)
#
#     plt.figure(figsize = (12, 5))
#     plt.subplots_adjust(wspace=0.4) # 서브 플롯 간에 가로 간격 설정
#     plt.subplot(1,2,1)
#
#     n = len(df['취미항목'].unique())
#     index = np.arange(n) # bar그래프 x축의 갯수(항목의 갯수만큼 설정)
#
#     plt.bar(index, df2, width = 0.35, color='b', alpha=0.5, label='2019')
#     plt.bar(index + 0.35, df3, width = 0.35, color='r', alpha=0.5, label='2020')
#     plt.title('연도에 따른 남성의 여가 활동')
#     plt.ylabel('활동 정도')
#     plt.xlabel('활동 분야')
#     plt.xticks(index, df1)
#     plt.legend()
#
#
#     dff = pd.read_csv("Project/Web/csv/1년_동안_가장_많이_참여한_여가활동(여성).csv")
#     dff2 = dff['2019'].values
#     dff3 = dff['2020'].values
#     print(dff2)
#
#     plt.subplot(1,2,2)
#     plt.bar(index, dff2, width = 0.35, color='b', alpha=0.5, label='2019')
#     plt.bar(index + 0.35, dff3, width = 0.35, color='r', alpha=0.5, label='2020')
#     plt.title('연도에 따른 여성의 여가 활동')
#     plt.ylabel('활동 정도')
#     plt.xlabel('활동 분야')
#     plt.xticks(index, df1)
#     plt.legend()
#     #plt.legend((p3[0], p4[0]), ('2019', '2020'))
#
#     fig = plt.gcf()
#     fig.savefig('Project/Web/static/graphs/hobbies.png')
#     return render(request, 'main2.html')

# def graph6Func(request):
#     delgraph()
#     df = pd.read_csv("Project/Web/csv/코로나_이후_전국_대중교통_이용량_변화(시내버스).csv", thousands=',')
#     df1 = df['구분'].values
#     df2 = df['2019'].values
#     df3 = df['2020'].values
#     df4 = df.loc[0, '2019']
#     df5 = df.loc[0, '2020']
#
#     print(df4+df5)
#
#     plt.figure(figsize = (18, 5))
#     plt.subplots_adjust(wspace=0.2) # 서브 플롯 간에 가로 간격 설정
#     plt.subplot(1,3,1)
#
#     n = len(df['구분'].unique())
#     index = np.arange(n)
#
#     plt.bar(index, df2, width = 0.35, color='b', alpha=0.5, label='2019')
#     plt.bar(index + 0.35, df3, width = 0.35, color='r', alpha=0.5, label='2020')
#     plt.title('연도에 따른 시도별 시내버스 이용')
#     plt.ylabel('이용건수(단위:10억)')
#     plt.xlabel('시/도')
#     plt.xticks(index, df1)
#     plt.legend()
#
#
#     dff = pd.read_csv("Project/Web/csv/코로나_이후_전국_대중교통_이용량_변화(광역, 철도).csv", thousands=',')
#     dff2 = dff['2019'].values
#     dff3 = dff['2020'].values
#     dff4 = df.loc[0, '2019']
#     dff5 = df.loc[0, '2020']
#     #print(dff2)
#
#     plt.subplot(1,3,2)
#     plt.bar(index, dff2, width = 0.35, color='b', alpha=0.5, label='2019')
#     plt.bar(index + 0.35, dff3, width = 0.35, color='r', alpha=0.5, label='2020')
#     plt.title('연도에 따른 시도별 광역/도시철도 이용')
#     plt.ylabel('이용건수(단위:10억)')
#     plt.xlabel('시/도')
#     plt.xticks(index, df1)
#     plt.legend()
#     #plt.legend((p3[0], p4[0]), ('2019', '2020'))
#
#     plt.subplot(1,3,3)
#     x_pie = [df4+dff4, df5+dff5]
#     labels = [2019, 2020]
#     plt.pie(x_pie, labels=labels,autopct='%.1f%%', counterclock=True, shadow =  True, explode=[0.03, 0.03])
#     plt.title('연도별 대중교통 총 이용량 비교')
#
#     fig = plt.gcf()
#     fig.savefig('Project/Web/static/graphs/hobbies.png')
#     return render(request, 'main2.html')

def graph7Func(request):
    delgraph()
    print('graph7Func 호출!!')
    df = pd.read_csv("Project/Web/csv/코로나19_이후_개인_소비_변화(성별).csv")
    print(df)
    df1 = df['성별'].values
    df2 = df['2019(사용액)'].values
    df3 = df['2020(사용액)'].values
    print(df2)
    n = len(df['성별'].unique())
    index = np.arange(n)
    
    plt.figure(figsize = (16, 8))
    plt.subplots_adjust(hspace=0.4)
    
    plt.subplot(2,2,1)
    plt.bar(index, df2, width = 0.35, color='#8c564b', alpha=0.7, label='2019')
    plt.bar(index + 0.35, df3, width = 0.35, color='#ff7f02', alpha=0.7, label='2020')
    plt.title('성별/연도에 따른 개인 소비액 변화')
    plt.ylabel('소비액')
    plt.xlabel('성별')
    plt.xticks(index, df1)
    plt.legend()
    
    df4 = df['2019(연체액)'].values
    df5 = df['2020(연체액)'].values
    plt.subplot(2,2,2)
    plt.bar(index, df4, width = 0.35, color='#8c564b', alpha=0.7, label='2019')
    plt.bar(index + 0.35, df5, width = 0.35, color='#ff7f02', alpha=0.7, label='2020')
    plt.title('성별/연도에 따른 개인 연채액 변화')
    plt.ylabel('소비액')
    plt.xlabel('성별')
    plt.xticks(index, df1)
    plt.legend()
    
    dff = pd.read_csv("Project/Web/csv/코로나19_이후_개인_소비_변화(연령별).csv")
    dff1 = dff['연령'].values
    dff2 = dff['2019(사용액)'].values
    dff3 = dff['2020(사용액)'].values
    print(dff2)
    n2 = len(dff['연령'].unique())
    index = np.arange(n2)
    
    plt.subplot(2,2,3)
    plt.bar(index, dff2, width = 0.35, color='darkcyan', alpha=0.7, label='2019')
    plt.bar(index + 0.35, dff3, width = 0.35, color='crimson', alpha=0.7, label='2020')
    plt.title('연령/연도에 따른 개인 소비액 변화')
    plt.ylabel('소비액')
    plt.xlabel('연령')
    plt.xticks(index, dff1)
    plt.legend()
    
    dff4 = dff['2019(연체액)'].values
    dff5 = dff['2020(연체액)'].values
    plt.subplot(2,2,4)
    plt.bar(index, dff4, width = 0.35, color='darkcyan', alpha=0.7, label='2019')
    plt.bar(index + 0.35, dff5, width = 0.35, color='crimson', alpha=0.7, label='2020')
    plt.title('연령/연도에 따른 개인 연채액 변화')
    plt.ylabel('소비액')
    plt.xlabel('연령')
    plt.xticks(index, dff1)
    plt.legend()
    
    fig = plt.gcf()
    fig.savefig('Project/Web/static/graphs/hobbies.png')
    return render(request, 'lifestyle.html')


def graph8Func(request):
    delgraph()
    df = pd.read_csv("Project/Web/csv/코로나_이후_취업자_실업자_데이터(수정).csv")
    print(df)
    df2 = df.drop(['구분'], axis=1) # 구분 컬럼만 삭제
    x = list(df2.columns)
    print(x) #['2019', '2020', '202105월', '202106월', '202107월', '202108월', '202109월', '202110월']
    n = len(df2.columns)
    index = np.arange(n)

    print(df.iloc[0, 1:].values)
    x1 = df.iloc[0, 1:].values  #[106.3 110.8 114.8 109.3 92.0 74.4 75.6 78.8] -> 실업자 수
    x2 = df.iloc[1, 1:].values #[38.6 37.0 40.2 38.6 30.8 24.3 22.3 23.4] -> 청년 실업자 수
    x3 = df.iloc[0:2, 0].values
    print(x3) # ['실업자' '청년실업자']
    
    plt.figure(figsize = (16, 5))
    plt.subplots_adjust(wspace=0.4)
    plt.subplot(1, 2, 1)
    plt.bar(index, x1, width = 0.35, color='#8c564b', alpha=0.7, label='실업자 수')
    plt.title('실업자 추이')  
    plt.ylabel('인구(만 명)')
    plt.xlabel('연도')
    plt.xticks(index, x)
    plt.legend()

    x4= df.iloc[3, 1:].values # [8.9 9.0 9.3 8.9 7.2 5.8 5.4 5.6] -> 청년 실업률
    x5= df.iloc[4, 1:].values # [3.8 4.0 4.0 3.8 3.2 2.6 2.7 2.8] -> 실업률
    ax = plt.twinx()
    ax.set_ylabel('실업률(%)')
    ax.plot(index, x5, color='deeppink', label='실업률')
    ax.legend(loc='lower right')
    #ax3 = plt.twinx()
    #ax3.plot(index, x5, color='crimson', label='3nd Data')
    #ax3.legend()

    # 실업자, 청소년 실업자 분리. 

    plt.subplot(1, 2, 2)
    plt.bar(index, x2, width = 0.35, color='#ff7f02', alpha=0.7, label='청년 실업자 수')
    plt.title('청년 실업자 추이')  
    plt.ylabel('인구(만 명)')
    plt.xlabel('연도')
    plt.xticks(index, x)
    plt.legend()

    ax = plt.twinx()
    ax.set_ylabel('청년 실업률(%)')
    ax.plot(index, x4, color='deeppink', label='청년 실업률')
    ax.legend(loc='lower right')
    
    fig = plt.gcf()
    fig.savefig('Project/Web/static/graphs/hobbies.png')
    return render(request, 'lifestyle.html')




#-----------데이터 분석!
def analysisFunc(request): # 데이터 분석 결과 넘겨주기.
    delgraph()
    file_name = 'Project/Web/static/graphs/analysis.png'
    if request.method == 'POST':
        v1 = request.POST.get("v1")
        v2 = request.POST.get("v2")
        v3 = request.POST.get("v3")
        
        def ols1featuremodel(x_data,x_label,title): # 독립변수 1개의 ols 모델. 단순 선형회귀
            df = pd.read_csv("Project/Web/csv/해외유입,확진자수,강남역,백신접종,검사자수,사망자수.csv", thousands=',')
            df = df[[x_data, '확진자수(당일)']]
            df = df.dropna(axis=0, how='any')
            #print(df)
            dfcorr = df.corr()
            print(dfcorr)
            #print('상관관계',dfcorr.iloc[1, 0]) # 상관관계
            corr = dfcorr.iloc[1, 0]
            
            #statsmodels ols 사용 
            x = df[x_data].values
            x = x.flatten()
            #print(x)
            y = df['확진자수(당일)'].values
            y = y.flatten()
            data = np.array([x, y])
            df = pd.DataFrame(data.T)
            df.columns = ['x1', 'y1']
            #print(df)
            result = smf.ols(formula = 'y1 ~ x1', data = df).fit()
            print(result.summary())
            print('결정계수(설명력):', result.rsquared) 
            print('p-value(유의확률):', result.pvalues[1]) 
            msg1 = '상관계수:{}'.format(corr)
            msg2 = '결정계수(설명력):{}'.format(result.rsquared)
            msg3 = 'p-value(유의확률):{}'.format(result.pvalues[1]) 
            msg = {'msg1' : msg1, 'msg2' : msg2, 'msg3' : msg3 }
            
            #시각화
            '''plt.scatter(x, y)
            plt.xlabel(x_label)
            plt.ylabel('확진자수(당일별)')
            xg = pd.DataFrame({'x1':[x.min(), x.max()]})
            print(xg)
            y_pred = result.predict(xg)
            
            plt.plot(xg, y_pred, c='r', label='모델의 추세선') # 추세선 표시
            plt.legend()
            plt.title(title)'''
            
            plt.figure(figsize = (6.5, 5))
            plt.xlabel('데이터 수')
            plt.ylabel('확진자수(당일별)')
            xg = df['x1']
            #print(xg)
            y_pred = result.predict(pd.DataFrame(xg))
            plt.plot(y, color='blue', label='실제값')
            plt.plot(y_pred, color='red', label='예측값')
            plt.title(title)
            plt.legend()
            return msg
        
        
        def ols2featuremodel(x1_data,x2_data,title): # 독립변수 2개의 ols 모델. 다중 선형회귀
            df = pd.read_csv("Project/Web/csv/해외유입,확진자수,강남역,백신접종,검사자수,사망자수.csv", thousands=',')
            # 2021-02-26 ~ 2021-11-16까지의 데이터.
            df = df[[x1_data, x2_data, '확진자수(당일)']]
            df = df.dropna(axis=0, how='any')
            #print(df)
            print(df.corr())
            dfcorr=df.corr()
            
            #statsmodels ols 사용
            x1 = df[x1_data].values
            x1 = x1.flatten()
            x2 = df[x2_data].values
            x2 = x2.flatten()
            
            y = df['확진자수(당일)'].values
            y = y.flatten()
            data = np.array([x1,x2, y])
            df = pd.DataFrame(data.T)
            df.columns = ['x1','x2','y1']
            print(df)
            result = smf.ols(formula = 'y1 ~ x1 + x2', data = df).fit()
            print(result.summary())
            print('결정계수(설명력):', result.rsquared_adj)
            print('p-value(유의확률):', result.pvalues[1]) 
            #msg = '결정계수(설명력):{}        p-value(유의확률):{}'.format(result.rsquared_adj, result.pvalues[1])
            msg1 = '결정계수(설명력):{}'.format(result.rsquared_adj)
            msg2 = 'p-value(유의확률):{}'.format(result.pvalues[1])
            #상관관계는 어떻게 보여주지....
            msg = {'msg1' : msg1, 'msg2' : msg2}
            
            # 시각화
            plt.figure(figsize = (6.5, 5))
            plt.xlabel('데이터 수')
            plt.ylabel('확진자수(당일별)')
            xg = df[['x1', 'x2']]
            #print(xg)
            y_pred = result.predict(pd.DataFrame(xg))
            plt.plot(y, color='blue', label='실제값')
            plt.plot(y_pred, color='red', label='예측값')
            plt.title(title)
            plt.legend()
            return msg
        
        
        def tensorflow1(x1, title): # 독립변수 1개에 대한 tensorflow 모델
            df = pd.read_csv("Project/Web/csv/해외유입,확진자수,강남역,백신접종,검사자수,사망자수.csv", thousands=',')
            df = df[[x1, '확진자수(당일)']]
            df = df.dropna(axis=0, how='any')
            #print(df)
            dfcorr = df.corr()
            #print('상관관계',dfcorr.iloc[1, 0]) # 상관관계
            corr = dfcorr.iloc[1, 0]
            x = df[x1].values
            x = x.flatten()
            x_list = list(x)
            x_data = np.array(x_list)
            print(x)
            print(x_data)
            y = df['확진자수(당일)'].values
            y = y.flatten()
            y_list = list(y)
            y_data = np.array(y_list)
            
            model = Sequential() 
            model.add(Dense(4, input_dim = 1, activation='linear'))
            model.add(Dense(16, activation='linear'))
            model.add(Dense(8, activation='linear'))
            model.add(Dense(1, activation='linear'))
            opti = optimizers.Adam(learning_rate = 0.01)
            model.compile(optimizer = opti, loss = 'mse', metrics = ['mae'])
            es = EarlyStopping(monitor='loss', mode='min', verbose=1, patience=50)
            history = model.fit(x=x_data, y=y_data, batch_size=50, epochs=100000, verbose=2, validation_split=0.2, callbacks=[es])                
            print(model.summary())
            y_pred = model.predict(x_data).flatten()
            print('예측값:', model.predict(x_data).flatten())
            #print(model.evaluate(x_data, y_data))
            #msg = '상관관계:{}        설명력(r2_score):{}'.format(corr, r2_score(y_data, y_pred))
            msg1 = '상관관계:{}'.format(corr)
            msg2 = '설명력(r2_score):{}'.format(r2_score(y_data, y_pred))
            msg = {'msg1' : msg1, 'msg2': msg2}
            # 시각화
            plt.figure(figsize = (6.5, 5))
            plt.xlabel('데이터 갯수')
            plt.ylabel('확진자수(당일별)')
            plt.plot(y, color='blue', label='실제값')
            plt.plot(y_pred, color='red', label='예측값')
            plt.title(title)
            plt.legend()          
            return msg
        
        
        def tensorflow2(x1,x2, title): # 독립변수 2개에 대한 tensorflow 모델
            df = pd.read_csv("Project/Web/csv/해외유입,확진자수,강남역,백신접종,검사자수,사망자수.csv", thousands=',')
            df = df[[x1, x2,'확진자수(당일)']]
            df = df.dropna(axis=0, how='any')
            #print(df)
            dfcorr = df.corr()
            #print('상관관계',dfcorr.iloc[1, 0]) # 상관관계
            x = df[[x1, x2]].values
            print(x)
            
            y = df['확진자수(당일)'].values
            #y = y.flatten()
            y_list = list(y)
            y_data = np.array(y_list)
            
            model = Sequential() 
            model.add(Dense(4, input_dim = 2, activation='linear'))
            model.add(Dense(16, activation='linear'))
            model.add(Dense(8, activation='linear'))
            model.add(Dense(1, activation='linear'))
            opti = optimizers.Adam(learning_rate = 0.01)
            model.compile(optimizer = opti, loss = 'mse', metrics = ['mse'])
            es = EarlyStopping(monitor='loss', mode='min', verbose=1, patience=50)
            history = model.fit(x = x, y=y_data, batch_size = 50, epochs = 10000, verbose=2,validation_split=0.2, callbacks=[es])
            print(model.summary())
            y_pred = model.predict(x).flatten()
            print('예측값:', model.predict(x).flatten())
            msg = {'msg1' : '설명력(r2_score):{}'.format(r2_score(y_data, y_pred))} 
            # 시각화
            plt.figure(figsize = (6.5, 5))
            plt.xlabel('데이터 갯수')
            plt.ylabel('확진자수(당일별)')
            plt.plot(y, color='blue', label='실제값')
            plt.plot(y_pred, color='red', label='예측값')
            plt.title(title)
            plt.legend()
            return msg
        
        
        if (v1=='level' and v2=="") or (v2=='level' and v1==""): # 독립변수가 강남역 일일 이용자수 1개일 경우
            # 2021-01-01 ~ 2021-10-31까지의 데이터.
            if v3 == 'ols':
                x_data = '강남역 승하차수(당일)'
                x_label = '강남역 승하차수(당일)'
                title = '독립변수가 강남역 일일 이용자수 1개일 경우'
                msg = ols1featuremodel(x_data,x_label,title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터. """
            else: # tensorflow
                x1 = '강남역 승하차수(당일)'
                title = '독립변수가 강남역 일일 이용자수 1개일 경우'
                msg = tensorflow1(x1,title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터."""
                                 
            
        elif (v1=='vaccination' and v2=="") or (v2=='vaccination' and v1==""): # 독립변수가 백신 접종률 1개일 경우
            # 2021-02-26 ~ 2021-11-16까지의 데이터.
            if v3 == 'ols': # ols
                x_data = '백신접종완료수(누적)'
                x_label = '백신접종완료자수(단위:천만)'
                title = '독립변수가 백신 접종률 1개일 경우'
                msg = ols1featuremodel(x_data,x_label,title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터. """
            else: # tensorflow
                x1 = '백신접종완료수(누적)'
                title = '독립변수가 백신 접종률 1개일 경우'
                msg = tensorflow1(x1,title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터"""

            
        elif (v1=='abroad' and v2=="") or (v2=='abroad' and v1==""): # 독립변수가 해외유입확진자 1개일 경우
            # 2021-01-01 ~ 2021-11-23까지의 데이터.
            if v3 == 'ols':
                x_data = '해외유입확진자'
                x_label = '해외유입확진자'
                title = '독립변수가 해외유입확진자 1개일 경우'
                msg = ols1featuremodel(x_data,x_label,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터. """
            else: # tensorflow
                x1 = '해외유입확진자'
                title = '독립변수가 해외유입확진자 1개일 경우'
                msg = tensorflow1(x1,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터. 
                """
        
        
        elif (v1=='check' and v2=="") or (v2=='check' and v1==""): # 독립변수가 검사수 1개일 경우
            if v3 == 'ols':
                x_data = '검사수(당일)'
                x_label = '검사 인구수(당일)'
                title = '독립변수가 검사수 1개일 경우'
                msg = ols1featuremodel(x_data,x_label,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터. """
            else: # tensorflow
                x1 = '검사수(당일)'
                title = '독립변수가 검사수 1개일 경우'
                msg = tensorflow1(x1,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터. 
                """
        
        elif (v1=='dead' and v2=="") or (v2=='dead' and v1==""): # 독립변수가 사망자수 1개일 경우
            if v3 == 'ols':
                x_data = '사망자수(당일)'
                x_label = '사망자 인구수(당일)'
                title = '독립변수가 사망자수 1개일 경우'
                msg = ols1featuremodel(x_data,x_label,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터. """
            else: # tensorflow
                x1 = '사망자수(당일)'
                title = '독립변수가 사망자수 1개일 경우'
                msg = tensorflow1(x1,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터. 
                """
        
        
        
        #-----독립변수가 2개 이상일 경우-----------
        elif (v1=='level' and v2=="vaccination") or (v2=='level' and v1=="vaccination"): # 독립변수가 강남역이용객, 백신접종률 2개일 경우
            # 2021-02-26 ~ 2021-10-31까지의 데이터.
            if v3 == 'ols':
                x1_data = '백신접종완료수(누적)'
                x2_data = '강남역 승하차수(당일)'
                title = '독립변수가 강남역이용객, 백신접종률 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-02-26 ~ 2021-10-31까지의 데이터."""
            else:
                x1 = '강남역 승하차수(당일)'
                x2 = '백신접종완료수(누적)'
                title = '독립변수가 강남역이용객, 백신접종률 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-02-26 ~ 2021-10-31까지의 데이터.
                """
        
        elif (v1=='level' and v2=="abroad") or (v2=='level' and v1=="abroad"): # 독립변수가 강남역이용객, 해외유입자 2개일 경우
            # 2021-01-01 ~ 2021-10-31까지의 데이터.
            if v3 == 'ols':
                x1_data = '해외유입확진자'
                x2_data = '강남역 승하차수(당일)'
                title = '독립변수가 강남역이용객, 해외유입자 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터."""
            else:
                x1 = '강남역 승하차수(당일)'
                x2 = '해외유입확진자'
                title = '독립변수가 강남역이용객, 해외유입자 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터.
                """
        
        elif (v1=='vaccination' and v2=="abroad") or (v2=='vaccination' and v1=="abroad"): # 독립변수가 백신접종률, 해외유입자 2개일 경우
            # 2021-02-26 ~ 2021-11-16까지의 데이터.
            if v3 == 'ols':
                x1_data = '백신접종완료수(누적)'
                x2_data = '해외유입확진자'
                title = '독립변수가 백신접종률, 해외유입자 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터."""
            else:
                x1 = '해외유입확진자'
                x2 = '백신접종완료수(누적)'
                title = '독립변수가 백신접종률, 해외유입자 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터.
                """           
        elif (v1=='level' and v2=="check") or (v2=='level' and v1=="check"): # 독립변수가 강남역이용객, 검사자수 2개일 경우
            # 2021-01-01 ~ 2021-10-31까지의 데이터.
            if v3 == 'ols':
                x1_data = '강남역 승하차수(당일)'
                x2_data = '검사수(당일)'
                title = '독립변수가 강남역이용객, 검사자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터.
                """
            else:
                x1 = '강남역 승하차수(당일)'
                x2 = '검사수(당일)'
                title = '독립변수가 강남역이용객, 검사자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터.
                """     
                
        elif (v1=='level' and v2=="dead") or (v2=='level' and v1=="dead"): # 독립변수가 강남역이용객, 사망자수 2개일 경우
            # 2021-01-01 ~ 2021-10-31까지의 데이터.
            if v3 == 'ols':
                x1_data = '강남역 승하차수(당일)'
                x2_data = '사망자수(당일)'
                title = '독립변수가 강남역이용객, 사망자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터.
                """
            else:
                x1 = '강남역 승하차수(당일)'
                x2 = '사망자수(당일)'
                title = '독립변수가 강남역이용객, 사망자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-01-01 ~ 2021-10-31까지의 데이터.
                """      
        
        elif (v1=='vaccination' and v2=="check") or (v2=='vaccination' and v1=="check"): # 독립변수가 백신접종자수(누적), 검사자수 2개일 경우
            # 2021-02-26 ~ 2021-11-16까지의 데이터.
            if v3 == 'ols':
                x1_data = '백신접종완료수(누적)'
                x2_data = '검사수(당일)'
                title = '독립변수가 백신접종자수(누적), 검사자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터.
                """
            else:
                x1 = '백신접종완료수(누적)'
                x2 = '검사수(당일)'
                title = '독립변수가 백신접종자수(누적), 검사자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터.
                """
        
        elif (v1=='vaccination' and v2=="dead") or (v2=='vaccination' and v1=="dead"): # 독립변수가 백신접종률, 사망자수 2개일 경우
            # 2021-02-26 ~ 2021-11-16까지의 데이터.
            if v3 == 'ols':
                x1_data = '백신접종완료수(누적)'
                x2_data = '사망자수(당일)'
                title = '독립변수가 백신접종률, 사망자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터.
                """
            else:
                x1 = '백신접종완료수(누적)'
                x2 = '사망자수(당일)'
                title = '독립변수가 백신접종률, 사망자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-02-26 ~ 2021-11-16까지의 데이터.
                """
          
          
        elif (v1=='abroad' and v2=="check") or (v2=='abroad' and v1=="check"): # 독립변수가 해외유입확진자수(당일), 검사자수 2개일 경우
            # 2021-01-01 ~ 2021-11-23까지의 데이터.
            if v3 == 'ols':
                x1_data = '해외유입확진자'
                x2_data = '검사수(당일)'
                title = '독립변수가 해외유입확진자수(당일), 검사자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터.
                """
            else:
                x1 = '해외유입확진자'
                x2 = '검사수(당일)'
                title = '독립변수가 해외유입확진자수(당일), 검사자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터.
                """       
        
        elif (v1=='abroad' and v2=="dead") or (v2=='abroad' and v1=="dead"): # 독립변수가 해외유입확진자수(당일), 사망자수 2개일 경우
            # 2021-01-01 ~ 2021-11-23까지의 데이터.
            if v3 == 'ols':
                x1_data = '해외유입확진자'
                x2_data = '사망자수(당일)'
                title = '독립변수가 해외유입확진자수(당일), 사망자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터.
                """
            else:
                x1 = '해외유입확진자'
                x2 = '사망자수(당일)'
                title = '독립변수가 해외유입확진자수(당일), 사망자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터.
                """              
            
        elif (v1=='check' and v2=="dead") or (v2=='check' and v1=="dead"): # 독립변수가 검사자수, 사망자수 2개일 경우
            # 2021-01-01 ~ 2021-11-23까지의 데이터.
            if v3 == 'ols':
                x1_data = '검사수(당일)'
                x2_data = '사망자수(당일)'
                title = '독립변수가 검사자수, 사망자수 2개일 경우'
                msg = ols2featuremodel(x1_data,x2_data,title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터.
                """
            else:
                x1 = '검사수(당일)'
                x2 = '사망자수(당일)'
                title = '독립변수가 검사자수, 사망자수 2개일 경우'
                msg = tensorflow2(x1,x2, title)
                msg2 = """2021-01-01 ~ 2021-11-23까지의 데이터.
                """
        fig = plt.gcf()
        fig.savefig(file_name)
    return render(request, 'main2.html',{'msg':msg,'msg2':msg2,'fig':fig, 'flag' : v3})

def saveFunc(request):
    name = request.GET.get('name')
    print(name)
    #C:/work/psou/
    im = Image.open('Project/Web/static/graphs/analysis.png')
    im.save('Project/Web/static/graphs/' + name + '.png')
    msg = '해당 이미지 저장되었습니다!'
    
    try: #name이 테이블에 있으면 등록 x
        Graph.objects.get(image = name) #입력한 이름을 가져와 검색
        return render(request, 'main2.html', {'msg':'이미 등록된 이미지 이름입니다.'})            
    except Exception as e:  #name이 다를 경우
        Graph(
            userid =  request.session.get('userid'),
            image = name
        ).save() # 입력한 것들을 저장(insert)
        
    return render(request, 'main2.html', {'msg':msg, 'fig':im})

def viewImageFunc(request):
    name = str(request.GET.get('image'))
    print(name)
    im = Image.open('Project/Web/static/graphs/' + name + '.png')
    im.save('Project/Web/static/graphs/' + name + '.png')
    msg1 = {'msg1' : name + ' 이미지 출력'}
    return render(request, 'main2.html', {'msg':msg1, 'fig':im})

