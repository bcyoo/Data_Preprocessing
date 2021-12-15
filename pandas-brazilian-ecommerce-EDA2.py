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

# ### pandas 라이브러리와 탐색적 데이터 분석 과정 익히기
#
# > 다양한 데이터 분석 케이스를 통해 데이터 분석과 pandas 라이브러리 활용에 대해 익히보기로 합니다.

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="3em" style="font-weight:bold;color:#3f8dbf;">탐색적 데이터 분석: 1. 데이터의 출처와 주제에 대해 이해</font><br>
#
# ### 전체 판매 프로세스
# 1. 해당 쇼핑몰에 중소업체가 계약을 맺고
# 2. 중소업체가 해당 쇼핑몰에 직접 상품을 올리고
# 2. 고객이 구매하면, 중소업체가 Olist가 제공하는 물류 파트너를 활용해서 배송을 하고,
# 3. 고객이 상품을 받으면, 고객에게 이메일 survey 가 전송되고,
# 4. 고객이 이메일 survey 에 별점과 커멘트를 남겨서 제출하게 됨
#     
# ### 데이터 출처
# - 브라질에서 가장 큰 백화점의 이커머스 쇼핑몰 (https://olist.com/)
#   - 2016년도부터 2018년도 9월까지의 100k 개의 구매 데이터 정보
#   - 구매 상태, 가격, 지불수단, 물류 관련, 리뷰관련, 상품 정보, 구매자 지역 관련 정보
#
# ### 주요 질문(탐색하고자 하는 질문 리스트)
# - **얼마나 많은 고객이 있는가?** 
# - **고객은 어디에 주로 사는가?** 
# - **고객은 주로 어떤 지불방법을 사용하는가?**
# - 평균 거래액은 얼마일까?
# - 일별, 주별, 월별 판매 트렌드는?
# - 어떤 카테고리가 가장 많은 상품이 팔렸을까?
# </div>

# ### 1. 얼마나 많은 고객이 있는가?

import pandas as pd
PATH = "00_data/"

products = pd.read_csv(PATH + "olist_products_dataset.csv", encoding='utf-8-sig')
customers = pd.read_csv(PATH + "olist_customers_dataset.csv", encoding='utf-8-sig')
geolocation = pd.read_csv(PATH + "olist_geolocation_dataset.csv", encoding='utf-8-sig')
order_items = pd.read_csv(PATH + "olist_order_items_dataset.csv", encoding='utf-8-sig')
payments = pd.read_csv(PATH + "olist_order_payments_dataset.csv", encoding='utf-8-sig')
reviews = pd.read_csv(PATH + "olist_order_reviews_dataset.csv", encoding='utf-8-sig')
orders = pd.read_csv(PATH + "olist_orders_dataset.csv", encoding='utf-8-sig')
sellers = pd.read_csv(PATH + "olist_sellers_dataset.csv", encoding='utf-8-sig')
category_name = pd.read_csv(PATH + "product_category_name_translation.csv", encoding='utf-8-sig')

customers.head()

customers.info()

# - value_counts(): 각각의 값이 전체 Series 에서 각각 몇 개가 있는지를 알려줌

customers['customer_unique_id'].value_counts().max()

customers['customer_id'].value_counts().max()

# - nunique(): unique 한 값의 갯수를 알려줌

customers['customer_id'].nunique()

customers['customer_unique_id'].nunique()

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="3em" style="font-weight:bold;color:#3f8dbf;">고객 분석1: 실제 고객 수는 99441 로 볼 수 있음</font><br>
# </div>

# ### 2. 고객은 어디에 주로 사는가?

customers.head()

customers_location = customers.groupby('customer_city').count().sort_values(by='customer_id', ascending=False)
customers_location.head(20)

customers_location = customers.groupby('customer_city')['customer_id'].nunique().sort_values(ascending=False)

customers_location.head(20)

import chart_studio.plotly as py
import cufflinks as cf
cf.go_offline(connected=True)

customers_location.iplot(kind='bar', theme='white')

customers_location_top20 = customers_location.head(20)

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="3em" style="font-weight:bold;color:#3f8dbf;">고객 분석2: 고객이 주로 사는 지역 TOP 20</font><br>
# </div>

customers_location_top20.iplot(kind='bar', theme='white')

customers_location_top20

top20_customer_locations = customers_location_top20.index

for index, location in enumerate(list(top20_customer_locations)):
    print ("TOP", index + 1, ":", location)

# <div class="alert alert-block" style="border: 1px solid #FFB300;background-color:#F9FBE7;">
# <font size="3em" style="font-weight:bold;color:#3f8dbf;">고객 분석3: 고객은 주로 어떤 지불방법을 사용할까?</font><br>
# </div>

payments.head()

# #### 없는 데이터 확인하기
# - isnull().sum() 사용

payments.isnull().sum()

# #### unique 한 값 확인하기
# - unique() 사용

payments['payment_type'].unique()

# #### 특정 값을 가진 행 삭제하기

payments = payments[payments['payment_type'] != 'not_defined']

payments['payment_type'].unique()

payment_type_count = payments.groupby('payment_type')['order_id'].nunique().sort_values(ascending=False)

payment_type_count

payment_type_count.iplot(kind='bar', theme='white')

# - 참고: https://plotly.com/python/pie-charts/

payment_type_count

# +
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(
    go.Pie(    
        labels=payment_type_count.index, values=payment_type_count.values
    )
)

fig.update_layout(
    {
        "title": {
            "text": "Payment Type Analysis",
            "font": {
                "size": 15
            }
        },
        "showlegend": True
    }
)

fig.show()
# -

# ### 그래프 세부 조정
# - 각 필드 확인: https://plotly.com/python/reference/

# +
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(
    go.Pie(    
        labels=payment_type_count.index, values=payment_type_count.values,
        textinfo='label+percent', insidetextorientation='horizontal'
    )
)

fig.update_layout(
    {
        "title": {
            "text": "Payment Type Analysis",
            "x": 0.5,
            "y": 0.9,
            "font": {
                "size": 15
            }
        },
        "showlegend": True
    }
)

fig.show()
# -






