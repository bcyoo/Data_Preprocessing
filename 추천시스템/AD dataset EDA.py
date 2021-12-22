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

# # Explorative Data Analysis on AD dataset

# ### Load libraries

import matplotlib.pyplot as plt 
## 이걸 세팅해주세요. 
plt.style.use(['dark_background'])

# %run lib.py

# ## Impression Logs (data/impression_log.csv)
# - imp_id: 노출 아이디
# - content_id: 광고 상품 아이디
# - server_time_kst: 로그(노출)생성 시간
# - bid_price: 광고 상품 입찰가 (PPC)
# - user_id: 노출 대상 사용자 아이디 (해쉬)
# - device_type: 노출 대상 디바이스 타입

# +
## dataset.csv
# label : 0은 노출됐지만 클릭되지 않는 것 / 1은 노출됐고 클릭이된 것
# -

impression_df = pd.read_csv('data/impression_log.csv')
impression_df.head()

# ### Bid Price Distribution

## 실제 노출된 광고의 bid_price
impression_df['bid_price'].describe()

sns.distplot(impression_df['bid_price'], bins=30)
## 대두분 50원에 분포한 것을 확인할 수 있다.

# ## View (Click) Logs (data/view_log.csv)
# - imp_id: 노출 아이디
# - server_time_kst: 로그(뷰) 생성 시간
# - bid_price: 클릭된 광고 상품 입찰가 (PPC)
# - device_type: 클릭 대상 디바이스 타입

# +
## click_log data
view_df = pd.read_csv('data/view_log.csv')
view_df.head()

## server_time_kst : 클릭이 발생한 시간
## 클릭이 발생했을 때의 bid_price
# -

# ### Bid Price Distribution

view_df['bid_price'].describe()

# +
sns.distplot(view_df['bid_price'], bins=30)

# 실제론 660원까지 bid 되었는데 실제로 클릭된것은 415원인 것을 확인
# -

# ## Advertiser (data/advertiser.csv)
# - user_id: 광고주 아이디
# - favorite_count: 광고주 선호수
# - grade: 광고주 등급
# - item_count: 광고주가 가지고 있는 상품수
# - interest: 광고주가 받은 클릭수
# - review_count: 광고주가 받은 리뷰수
# - comment_count: 광고주가 작성한 코멘트수
# - follower_count: 광고주의 팔로워수
# - pay_count: 광고주의 결제시스템 거래수
# - parcel_post_count: 광고주의 택배거래수
# - transfer_count: 광고주의 거래수
# - chat_count: 광고주의 채팅수

## 광고주 data
advertiser_df = pd.read_csv('data/advertiser.csv')
advertiser_df.head()

# ### Advertiser Feature Distribution

# +
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(20, 16))
fig.subplots_adjust(hspace=0.5)
fig.suptitle('distributions of advertiser')

for ax, feature, name in zip(axes.flatten(), advertiser_df.T.values.tolist(), list(advertiser_df.columns)):
    sns.distplot(feature, ax=ax, bins=20)
    ax.set(title=name)
    
    
    ## item_count :  일부 광고주들은 많은 아이템을 갖는 경우가 있음
# -

# ## User (data/viewer.csv)
# - user_id: 클릭한 사용자 아이디 (해쉬)
# - gender: 클릭한 사용자 성별
# - grade: 클릭한 사용자 나이
# - following_cnt: 상품 노출 대상의 팔로잉 수
# - pay_count: 상품 노출 대상의 거래수
# - parcel_post_count: 상품 노출 대상의 택배 거래수
# - transfer_count: 상품 노출 대상의 송금 거래수

## user data
viewer_df = pd.read_csv('data/viewer.csv')
viewer_df.head()

# ### User Feature Distribution

# +
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(20, 12))
fig.subplots_adjust(hspace=0.5)
fig.suptitle('distributions of viewer')

for ax, feature, name in zip(axes.flatten(), viewer_df.T.values.tolist(), list(viewer_df.columns)):
    sns.distplot(feature, ax=ax, bins=20)
    ax.set(title=name)
    
    
    ## age : 20~30대 분포가 가장 많음
# -

# ## AD (data/ad.csv)
# - content_id: 광고 상품 아이디
# - name: 광고 상품 이름
# - keyword: 광고 상품 태그
# - price: 광고 상품 가격
# - flag_used: 광고 상품 중고 여부
# - category_id_1: 광고 상품 1차 카테고리
# - category_id_2: 광고 상품 2차 카테고리
# - category_id_3: 광고 상품 카테고리
# - emergency_cnt: 광고 상품 신고수
# - comment_cnt: 광고 상품에 달린 코멘트수
# - interest: 광고 상품 클릭수
# - pfavcnt: 광고 상품 좋아요 수

## 광고에 대한 정보
ad_df = pd.read_csv('data/ad.csv')
ad_df.head()

# +
ad_stat_df = ad_df[['price', 'flag_used', 'category_id_1', 'category_id_2', 'category_id_3', 'comment_cnt', 'interest', 'pfavcnt']]
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(20, 12))
fig.subplots_adjust(hspace=0.5)
fig.suptitle('distributions of ad')

for ax, feature, name in zip(axes.flatten(), ad_stat_df.T.values.tolist(), list(ad_stat_df.columns)):
    sns.distplot(feature, ax=ax, bins=20)
    ax.set(title=name)


# 



