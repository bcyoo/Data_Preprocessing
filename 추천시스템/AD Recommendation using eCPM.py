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

# # AD Recommendation using eCPM

# ### Load libraries

# %run lib.py

# ## Load Model

model = joblib.load('model.pkl')

# ## Load Candidate ADs

# +
df = pd.read_csv('data/dataset.csv')

## 상위 1000개, 중복제거 (기준 : content_id)
candidates = df[:1000].drop_duplicates(['content_id'], keep='first')

candidates_df = candidates[candidate_features]
candidates_df.reset_index(drop=True, inplace=True)
candidates_df.head()
# -

candidates_df.to_csv('candidates_df.csv')

# ## Create User Data

## 임의 user data
user_demo = pd.DataFrame({
    'c_user_gender': [1],  ## 2은 남성, 1은 여성
    'c_user_age': [34],
    'user_following_count': [20],
    'user_pay_count': [30],
    'user_parcel_post_count': [1],
    'user_transfer_count': [1],
    'user_chat_count': [10]
})

# ## Generate Input Feature Data

## 실제 클릭예측에 사용할 수 있는 DF
feature_df = user_demo.merge(candidates_df, how='cross')
feature_df.head()

# ### Process missing values

## 결측값 제거 
feature_df = process_missing_values(feature_df)

# ### Predict Clicks

# +
# 클릭 예측
feature_df = feature_df[features]
probs = model.predict_proba(feature_df)

candidates_df['probs'] = probs[:, 1] # 전체 행에대해서 첫번째 컬럼  0클릭 안할 확률 / 1 클릭할 확률
candidates_df.head()
# -

# ### Compute eCPM and sort by eCPM
# eCPM = pClick * BidPrice * 1000
#  - bid_price와 click을 예측하고 1000번 노출했을 때 얼마나 수익을 기대할수 있느냐 = eCPM

## ecpm 컬럼을 추가하고 bid_price * pClick * 1000번 노출
candidates_df['ecpm'] = candidates_df['content_bid_price'] * candidates_df['probs'] * 1000

## eCPM이 높은 순으로 정렬
candidates_df.sort_values(by=['ecpm'], ascending=False, inplace=True)
candidates_df.head()

# ### Display Recommended AD Results

# +
from IPython.display import HTML, display

html = ""
for idx, row in candidates_df[0:20].iterrows():
    html += f'''
        <div style="display:inline-block;min-width:150px;max-width:150px;vertical-align:top">
        <ul>
            <li>eCPM: {row.ecpm}</li>
            <li>bid: {row.content_bid_price}</li>
            <li>prob: {row.probs}</li>
        </ul>
        <img src="{row.content_img_url}" style="width:150px;">
        </div>
        '''
    
display(HTML(html))
# 




