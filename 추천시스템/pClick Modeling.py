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

# # pClick Modeling

# ### Load libraries

import matplotlib.pyplot as plt 
## 이걸 세팅해주세요. 
plt.style.use(['dark_background'])

# %run lib.py

# ## Load Training Dataset

## 실제 label이 부여되어있고, 실제로 클릭 예측할 때 필요한 정보, 이미지 url도 갖고잇음.
df = pd.read_csv('data/dataset.csv')
df.head()

# ### Average CTR

# +
grouped_label = df.groupby('label').size()
average_ctr = float(grouped_label[1]/grouped_label.sum())
average_ctr

## 평균 ctr은 2.4%
# -

# ## Process missing values

## 결측값들을 처리가 만든 process_missing_values로 categorycal data와 continuous data  결측값 전처리
df = process_missing_values(df)

# ## Split into Train and Test data (8:2)

# +
# categorical = [
#     'c_user_gender', : 클릭한 사용자 성별
#     'c_user_age',    : 클릭한 사용자 나이
#     'c_content_flag_used', 광고 상품 중고 여부
#     'c_content_category_id_1',  광고 상품1차 카테고리
#     'c_content_category_id_2',  광고 상품2차 카테고리
#     'c_content_category_id_3']  광고 상품3차 카테고리



# continuous = [
#     'user_following_count', : 상품 노출 대상의 팔로잉 수
#     'user_pay_count',       : 상품 노출 대상의 거래수
#     'advertiser_grade',     : 광고주 등급
#     'advertiser_item_count',   : 광고주가 갖고 있는 상품수 
#     'advertiser_interest_count',  : 광고주가 받은 클릭 수
#     'advertiser_follower_count',  : 광고주의 팔로워 수
#     'advertiser_pay_count',       : 광고주의 결제시스템 거래수
#     'advertiser_review_count',    : 광고주가 받은 리뷰 수
#     'advertiser_parcel_post_count', : 광고주의 택배 거래수
#     'advertiser_transfer_count',    : 광고주의 거래 수
#     'advertiser_chat_count',        : 광고주의 채팅 수
#     'advertiser_favorite_count',    : 광고주 선호 수
#     'advertiser_comment_count',     : 광고주가 작성한 코멘트 수 
#     'content_bid_price',            : 광고 상품 입찰가 PPC
#     'content_price',                : 광고 상품 가격
#     'content_emergency_count',      : 광고 상품 신고수
#     'content_comment_count',        : 광고 상품에 달린 코멘트 수
#     'content_interest_count',       : 광고 상품 클릭수
#     'content_favorite_count']       : 광고주 선호 수

# +
train_test_df = df[['label'] + features]  
train, test = train_test_split(train_test_df, test_size = 0.2) ## 주어진 비율로 train, test 0.2 비율로 나눔

X_train = train[features]  #실제 input은 features
y_train = train['label']   # output은 label

X_test = test[features]
y_test = test['label']
# -

# # Build Model

# +
model = lgb.LGBMClassifier(n_estimators=1000,
    learning_rate=0.1,
    num_leaves=100,
    max_depth=15,
    zero_as_missing=True,
    n_jobs=os.cpu_count(),
    objective='binary')

model.fit(X=X_train, y=y_train)
# -

# # Evaluate the Trained Model

# +
avg_ctr = average_ctr
prior = log_loss(y_train, [avg_ctr]*len(y_train))

pred = model.predict_proba(X_test)[:, 1]
classifier = log_loss(y_test, pred)

rig = (prior - classifier) / prior

print(f"Baseline: {avg_ctr}")
print(f"RIG: {rig}")
# -

# ### See feature importance

fig, ax = plt.subplots(figsize=(15, 10))
lgb.plot_importance(model, ax=ax)

# 'c_user_age'                   : 클릭한 사용자 나이
# 'user_following_count',        : 상품 노출 대상의 팔로잉 수
# 'content_price'                : 광고 상품 가격
# 'content_interest_count'       : 광고 상품 클릭수
# 'content_bid_price'            : 광고 상품 입찰가 PPC
# 'content_favorite_count'       : 광고주 선호 수    
# 'user_pay_count'               : 상품 노출 대상의 거래수
# 'c_user_gender'                : 클릭한 사용자 성별
# 'advertiser_grade'             : 광고주 등급
# 'advertiser_comment_count'     : 광고주가 작성한 코멘트 수 
# 'advertiser_item_count'        : 광고주가 갖고 있는 상품수
# 'advertiser_pay_count'         : 광고주의 결제시스템 거래수
# 'content_comment_count'        : 광고 상품에 달린 코멘트 수
# 'advertiser_interest_count'    : 광고주가 받은 클릭 수
# 'content_emergency_count'      : 광고 상품 신고수
# 'advertiser_chat_count'        : 광고주의 채팅 수
# 'advertiser_favorite_count'    : 광고주 선호 수
# 'advertiser_transfer_count'     : 광고주의 거래 수
# 'c_content_category_id_2'       : 광고 상품2차 카테고리    
# 'advertiser_parcel_post_count'  : 광고주의 택배 거래수
# 'c_content_category_id_1'       : 광고 상품1차 카테고리
# 'c_content_category_id_3'       : 광고 상품3차 카테고리
# 'c_content_flag_used'           : 광고 상품 중고 여부
# 'advertiser_review_count'      : 광고주가 받은 리뷰 수


# ### Dump the model

joblib.dump(model, 'model.pkl')


