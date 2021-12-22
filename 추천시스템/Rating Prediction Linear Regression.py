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

# # Rating Prediction using Linear Regression

# +
# %run liblecture.py

import math
import numpy as np
from numpy import linalg as LA
import pandas as pd
# -

np.set_printoptions(precision=2)
pd.set_option('display.precision', 2)

# ## Movie Feature Matrix

movies = pd.read_csv('movielens/movies_w_imgurl.csv')
movies.head()

# genre의 row값들을 컬럼으로 변경
movieGenres = pd.DataFrame(data=movies['genres'].str.split('|').apply(pd.Series, 1).stack(), columns=['genre'])
movieGenres.index = movieGenres.index.droplevel(1)
movieGenres

## unique한 장르값 출력 (20개)
genres = movieGenres.groupby('genre').count()
genres

# +
movieWeights = pd.DataFrame(data=movies['movieId'])

for genre in genres.index:
    df = pd.DataFrame(data = movieGenres[movieGenres['genre'] == genre], columns=[genre])
    df[genre] = 1
    movieWeights = movieWeights.join(df, on='movieId')

movieWeights.fillna(0, inplace=True)

movieWeights
## 장르에 대해서
# -

# ## Make Regression Model for Users

# +
ratings = pd.read_csv('ratings-9_1.csv')

train = ratings[ratings['type'] == 'train'][['userId', 'movieId', 'rating']]
test = ratings[ratings['type'] == 'test'][['userId', 'movieId', 'rating']]

# +
userId = 33

userRatings = train[train['userId'] == userId][['movieId', 'rating']] 
userRatings = userRatings.sort_values(by='movieId')
userRatings
# -

#movieWeights['movieId'] 안에 userRatings['movieId'] isin 찾기
userLRTrain = movieWeights[movieWeights['movieId'].isin(userRatings['movieId'].values)]
userLRTrain

## movieId에 대해 sort_values
userLRTrain = movieWeights[movieWeights['movieId'].isin(userRatings['movieId'].values)].sort_values(by='movieId')
userLRTrain

## userLRTrain.iloc[L,1:] > input parameter
## parameter때문에 실제 학습에는 [:, 1:]사용해서 matrix 형태로 주어야함 
X = userLRTrain.iloc[:, 1:].values
X

Y = userRatings['rating'].values
Y

# ### Linear Regression
# http://scikit-learn.org/stable/modules/linear_model.html

from sklearn import linear_model as lm
reg = lm.LinearRegression()
reg.fit(X, Y) # x:input / y:output

print(reg.coef_) ## 각각의 장르에 대한 w 값
print(reg.intercept_) ## bois 값

## userTest data
userTestRatings = pd.DataFrame(test[test['userId'] == userId])
userTestRatings

# movieWeights에서 userTestRatings['movieId']를 isin 해서 input 값으로 사용
movieWeights[movieWeights['movieId'].isin(userTestRatings['movieId'].values)]

# input 값으로 사용하기 위해 movieId를 제거하고 arr형태로 변경
# reg.predict 해서 pred 값이 예측된 값으로 출력됨
pred = reg.predict(movieWeights[movieWeights['movieId'].isin(userTestRatings['movieId'].values)].iloc[:,1:].values)
pred

# +
userTestRatings['pred'] = pd.Series(data=pred, index = userTestRatings.index)

userTestRatings

# +
## MAE 값 / RMSE 값
mae = getMAE(userTestRatings['rating'], userTestRatings['pred'])
rmse = getRMSE(userTestRatings['rating'], userTestRatings['pred'])

print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

## 단순한 cbf 대비 개선됨을 확인할 수 있었음. / 제한된 genre feature 갖고 학습 경우에 효과가 있음을 확인됨
## 실제 추천에서는 LR를 사용해서 예측 경우는 많지 않음 (w값 학습할 때 사용함)
