import pandas as pd
import numpy as np
import konlpy.jvm
import re
from konlpy.tag import Okt
from collections import Counter
from konlpy.tag import Mecab
import itertools

from konlpy.tag import Kkma
from collections import Counter
from konlpy.tag import Kkma
import openpyxl
from sklearn.feature_extraction.text import CountVectorizer
import re
import konlpy
import math
import time


        ###################전처리###########################

df=pd.DataFrame(pd.read_excel("C:/Users/icako/Desktop/News.xlsx"))
df=df.fillna(" ") ## 공란을 공백으로 대체

Datecount=df.groupby("Date").count().sort_values(by="Title",ascending=False) ## 일자별 기사 개수

df["Corpus"]=df['Title']+df['Body'] ## 기사 제목과 본문의 내용을 합친 말뭉치 생성

stopwords = pd.read_csv(
"https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt").values.tolist() ## 한국어에서 높은 빈도로 사용되는 불용어 리스트

def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')  # 정규 표현식 처리
    result = hangul.sub('', text)
    okt = Okt()  # 형태소 추출
    nouns = okt.nouns(result)
    nouns = [x for x in nouns if len(x) > 1]  # 한글자 키워드 제거
    nouns = [x for x in nouns if x not in stopwords]  # 앞서 로드한 데이터를 기반으로 하여 불용어 제거
    return nouns

pd.set_option('mode.chained_assignment',  None)

start = time.time()

df['Nouns']=""

for i in range(0,len(df)+1):

    df['Nouns'][i]=text_cleaning(df['Corpus'][i])
    print(str(i)+'/'+str(len(df)))

end = time.time()
result = datetime.timedelta(seconds=end - start)

df.to_pickle("Nouns2.pkl") ##각 말뭉치에 있는 명사 okt 사전을 사용하여 추출.

okt.nouns("원태인은 삼성 라이온즈 소속의 투수이다")

###kt 사용자 사전에 KBO 선수의 이름을 대거 추가해주었고, 그 결과 선수 이름이 명사로써 잘 추출이 되고 있다. **###

okt.nouns("KIA 타이거즈")


import pickle
import pandas as pd

df2=pd.DataFrame(pd.read_pickle("C:/Users/icako/PycharmProjects/KBOtrend/Nouns2.pkl"))

import datetime as dt

from datetime import datetime


df2["Date"]=pd.to_datetime(df2["Date"],format='%Y%m%d')

players=pd.DataFrame(pd.read_csv("KBOPlayers.csv",encoding="CP949")) ## 선수명 언급 빈도 저장

for i in range(1,13):
    players[i]=""

for j in range(0,len(players)+1):
    for i in range(1,13):
        count = 0
        for k in df2.Nouns[df2["Date"].dt.month==i]:
            if players.이름[j] in k:
                count=count+1   ## 선수별 언급 빈도 계산
        players[i][j]=count
        print(str(j)+'/'+str(len(players))+" "+str(i)+"/"+"12")

players.to_csv("Player_Trend2.csv",index_label=False,encoding="CP949")


Team=["트윈스","랜더스","이글스","히어로즈","라이온즈","타이거즈","자이언츠","다이노스","위즈","베어스","와이번스"]

TeamT=pd.DataFrame(Team,columns=['Teamname'])  ## 팀명 언급 빈도 저장

for i in range(1,13):
    TeamT[i]=""

for j in range(0,len(TeamT)+1):
    for i in range(1,13):
        count = 0
        for k in df2.Nouns[df2["Date"].dt.month==i]:
            if TeamT.Teamname[j] in k:
                count=count+1  #팀명 별 언급 빈도 계산
        TeamT[i][j]=count
        print(str(j)+'/'+str(len(TeamT))+" "+str(i)+"/"+"12")

TeamT.to_csv("Team_Trend2.csv",index_label=False,encoding="CP949")


Corp=["LG","SSG","한화","키움","삼성","KIA","롯데","NC","KT","두산","SK"]

CorpT=pd.DataFrame(Corp,columns=['Corpname'])

for i in range(1,13):
    CorpT[i]=""

for j in range(0,len(CorpT)+1):
    for i in range(1,13):
        count = 0
        for k in df2.Corpus[df2["Date"].dt.month==i]:
            if CorpT.Corpname[j] in k:
                count=count+1 ## 기업명별 언급빈도 계산
        CorpT[i][j]=count
        print(str(j)+'/'+str(len(CorpT))+" "+str(i)+"/"+"12")


CorpT.to_csv("Corp_Trend.csv",index_label=False,encoding="CP949")   ## 기업명 언급 빈도 저장