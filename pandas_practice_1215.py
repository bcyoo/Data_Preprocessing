# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ### 연습문제와 추가 문법으로 정리하는 pandas

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">1. 00_data/olist_customers_dataset.csv 파일 pandas dataframe 으로 읽어오기 (데이터프레임 변수 이름은 doc 로 하기로 함)</font><br>
# </div>    

# +
import pandas as pd

doc = pd.read_csv('00_data/olist_customers_dataset.csv', encoding='utf-8-sig')
doc.head()
# -

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">2. 처음 5개 열 확인하기</font><br>
# </div>    

doc.head()

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">3. 전체 record 수(행 수) 확인하기</font><br>
# </div>    

doc.shape

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">4. 전체 열의 수 확인하기</font><br>
# </div>    

doc.info()

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">5. 열의 이름 리스트로 가져오기</font><br>
# </div>    

doc.columns

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">6. 인덱스 확인하기</font><br>
# </div>    

doc.index

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">7. 다섯 숫자 요약(5 number summary) 확인하기 </font><br>
# </div>    

doc.describe()

# ### 추가 문법 pandas.DataFrame.copy
# - 데이터프레임 중 일부를 선택 후, 조작하면 해당 데이터프레임도 변경
# - copy() 를 통해, 복사본을 만들어서 조작하여, 원본 데이터프레임은 보존 가능

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">8. customer_zip_code_prefix, customer_city, customer_state 컬럼만 가져오기 (데이터프레임 변수 이름은 doc2로 하기로 함)</font><br>
# </div>    

doc2 = doc[['customer_zip_code_prefix','customer_city','customer_state']].copy()
doc2
## doc2 복사본이 생김.

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">9. customer_city 가 sao paulo 인 레코드(행)만 가져오기 (데이터프레임 변수 이름은 doc3 으로 하기로 함)</font><br>
#     - 레코드(행) 수 확인도 해보기
# </div>    

doc3 = doc2[doc2['customer_city']=='sao paulo']
doc3.shape

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">10. customer_city 기준으로 행의 갯수를 확인해보세요 </font><br>
#     - doc2에 value_counts() 를 써보세요 (value_counts() 는 Series 에만 적용 가능합니다.) <br>    
# </div>

doc2['customer_city'].value_counts()

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">11. doc 데이터프레임에서 customer_city 기준으로 행의 갯수를 확인해보세요 </font><br>
#     1. groupby 를 써서 customer_city 를 기준으로 행의 갯수를 count 하세요 (새로운 데이터프레임 변수 이름은 doc4로 하기로 함)<br>
#     2. doc4를 통해 customer_city 수도 확인해보세요 (데이터프레임 레코드(행) 수를 확인해보면 됩니다.)<br>
# </div>

doc

doc4 =doc.groupby('customer_city').count()
doc4
## groupby를 하게되면 customer_city를 기준으로 a부터 자동정렬이됨

## DF row
# doc4.shape
len(doc4.index)

# ### 추가 문법 이해 (정렬, sort_values(), sort_index())
# 1. groupby(기준컬럼) 계산시, 기준컬럼은 인덱스로 설정이 되고, 해당 컬럼값을 기반으로 자동 정렬됨
# 2. 데이터프레임.sort_values(by=컬럼명, ascending=False) 
#    - ascending=True: 오름차순 (디폴트)
#    - ascending=False: 내림차순
# 3. 시리즈.sort_values(ascending=True)
# 4. 데이터프레임/시리즈.sort_index(ascending=True): 인덱스 기준 정렬

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">12. doc4에서 가장 레코드(행)의 수가 많은 customer_city 를 확인해보세요</font><br>
#     1. doc4의 customer_id 를 기준으로 정렬하고, 가장 상단의 한 행만 출력하기<br>
# </div>

doc4

doc4.sort_values(by='customer_id', ascending=False)

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">13. doc 에서 customer_city 를 인덱스로 만들고, 알파벳 순으로 인덱스를 정렬해보세요</font><br>
# </div>

doc

doc.set_index('customer_city').sort_index()
## index 동일한 값들이 남음, 알파벳으로 정렬하려면 sort_index

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">14.  doc2에서 customer_state 기준으로 행의 갯수를 확인해보세요</font><br>
#    - doc2에 value_counts() 를 써보세요 (value_counts() 는 Series 에만 적용 가능합니다.) <br>    
# </div>   

doc2

doc2['customer_state'].value_counts()

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">15. doc2에서 customer_state 갯수를 확인해보세요</font><br>
# </div>   

doc2['customer_state'].value_counts().shape

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">16. doc4에서 customer_city 갯수가 1000개 이상인 customer_city 갯수만 확인해보세요</font><br>
# </div>   

# +
import pandas as pd

doc = pd.read_csv('00_data/olist_customers_dataset.csv', encoding='utf-8-sig')
doc4 = doc.groupby('customer_city').count()
doc4.head()
# -

doc4[doc4['customer_id'] >1000].shape
#customer_id 개가 1000개 이상인 경우 수

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">17. doc4에서 customer_city 갯수가 1000개 이상인 customer_city 이름을 확인해보세요</font><br>
# </div> 

doc4[doc4['customer_id'] >1000].index

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">18. doc에서 결측치가 각 컬럼에 있는지 확인해보세요</font><br>
# </div> 

doc.isnull().sum()

# ### 추가 문법 이해 (to_list())
# 1. 시리즈.to_list()
#    - 컬럼값을 리스트 타입으로 리턴

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">19. doc에서 중복된 customer_city 를 가진 행을 삭제한 후, customer_city 이름만 가져와보세요</font><br>
# </div> 

doc

doc.drop_duplicates(subset='customer_city')['customer_city'].to_list()

# ### 추가 문법 이해 (pivot_table)

# - pivot_table(데이터프레임, values=None, index=None, aggfunc='mean', fill_value=None, margins=False, margins_name='All')
#   - values: 분석할 열 이름 리스트
#   - index: 인덱스로 들어갈 키 열
#   - aggfunc: 계산 방법, 간단히 {분석할열이름:계산방법} 으로 사전 형식으로 작성
#     - 주요 계산 방법: sum(합), mean(평균), median(중앙값), std(표준편차)
#   - fill_value: 결측치 대체 값
#   - margins: 모든 데이터의 총 분석 결과를 추가함 (예, 총 합)
#   - margins_name: 모든 데이터의 총 분석 결과의 이름

# +
import pandas as pd

doc_covid = pd.read_csv('COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/04-01-2020.csv', encoding='utf-8-sig')
doc_covid.head()
# -

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">20. doc_covid 에서 중복된 Country_Region 각각에 대해 Confirmed 를 모두 더한 값을 컬럼으로 갖는 데이터프레임을 피봇테이블로 만드세요</font><br>
# - 결측치는 0으로 만드세요
# </div> 

## doc_covid df에 Country_Region컬럼의 중복된 나라를 기준을 해서 Confirmed 대해서 동일한 국가는 합치겠다
## index에는 키가 될 Country_Region가 리스트[]로 들어가고,
## Confirmed 컬럼을 계산한 것은 values에 들어가고,
## Confirmed 중복된 나라들을 어떻게 계산할지는 aggfunc에 전체에 대한 중 중앙값으로 나타냄
## fill_value는 0으로 대체
## 
doc_covid2 = pd.pivot_table(doc_covid, 
                            index=['Country_Region'], 
                            values=['Confirmed'],
                            aggfunc={'Confirmed': 'median'}, 
                            fill_value=0,
                            margins=True,
                            margins_name='Total'
                           )
doc_covid2.head()

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="2em" style="font-weight:bold;color:#3f8dbf;">21. doc_covid 에서 중복된 Country_Region 각각에 대해 Confirmed 를 모두 더한 값을 컬럼으로 갖는 데이터프레임을 피봇테이블로 만들고, 총 값을 'Total' 을 인덱스 값으로 하는 record 로 추가하세요</font><br>
# - 결측치는 0으로 만드세요
# </div> 

doc_covid2 = pd.pivot_table(doc_covid, 
                            index=['Country_Region'], 
                            values=['Confirmed'],
                            aggfunc={'Confirmed': 'median'}, 
                            fill_value=0,
                            margins=True,
                            margins_name='Total'
                           )
doc_covid2


