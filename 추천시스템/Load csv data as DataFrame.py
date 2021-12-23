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

# # Recommendation System Exercise 2.1
#

# Import Packages

# +
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import math
## 이걸 세팅해주세요. 
plt.style.use(['bmh'])
# -

# Load csv data as DataFrame

## 영화 평점 csv 파일 불러오기.
df = pd.read_csv('movielens/ratings.csv')
df

# Check shape and columns of the DataFrame.
#
# See examples rows at the head and tail.

df.head(5)

df.tail(5)

print(df.shape)  ## shape 확인.
print(df.columns)  ## 컬럼명 확인.

## userId movieId rating 10에서 15번째 특정 row 출력
df[['userId', 'movieId', 'rating']].iloc[10:15]

# Convert timestamp as datetime.datetime and add year column.

df['timestamp']

## pd.to_datetime으로 변경 초 단위로 unit ='s' 로 변경함
pd.to_datetime(df['timestamp'].astype(int), unit='s')

## date 컬럼을 만들고 초 단위로 추가됨
df['date'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
## 년도 별로 추출함.
df['year'] = df['date'].apply(lambda x: x.year)
df

# Count ratings per year and show a bar chart.

## 년도별로  groupby를 통해 row을 출력
yearCounts = df.groupby('year').size()
yearCounts.columns = ['counts']
yearCounts = pd.DataFrame(data = yearCounts, columns = ['counts'])
yearCounts

yearCounts.plot(kind='bar', figsize=(12, 8), label='counts', legend=True)

# Divide rating data into train and test data.

## DF의 Train을 sample 이라는 방식을 사용해서 90% 추출함
train = df.sample(frac=0.9, random_state=1)
train['type'] = 'train'
train.head()

test = df.drop(train.index)
test['type'] = 'test'
test.head()

# Compute average rating of all users and assign it to the all predicted ratings.

## train의 평점의 평균
avgRating = train['rating'].mean()
avgRating

avgPred = test[['userId', 'movieId', 'rating']].copy()
## user와 상관없이 pred을 넣어줌
avgPred['pred'] = avgRating
avgPred.head()

# Compute MAE and RMSE for the average rating prediction result.

## MAE , RMSE 구하기
avgPredErrors = avgPred['pred'] - avgPred['rating']
## MAE는 절대값취하고 평균값을 구함
mae = avgPredErrors.abs().mean()
## RMSE 
rmse = math.sqrt(avgPredErrors.pow(2).mean())
print(mae)
print(rmse)

# Compute average rating of each user and assign them to the predicted ratings of each user.

## train에서 userid와 그 user의 rating을 추출
## user 기준으로 groupby하고 agg('mean') 하면 각 유저별 평균 rating 값을 알 수 있음
userAvgRatings = train[['userId', 'rating']].groupby('userId').agg('mean')
userAvgRatings.columns = ['pred'] ## 평균을 pred값이라고 함
userAvgRatings

userAvgPred = test[['userId', 'movieId', 'rating']]
## userAvgRatings를 userAvgPred merge해서 DF를만듬, 
userAvgPred = pd.merge(userAvgPred, userAvgRatings, how='left', left_on=['userId'], right_on=['userId'], right_index = False)
userAvgPred.head()


userAvgPredErrors = userAvgPred['pred'] - userAvgPred['rating']
mae2 = userAvgPredErrors.abs().mean()
rmse2 = math.sqrt(userAvgPredErrors.pow(2).mean())
print(mae2)
print(rmse2)

# Compute MAE and RMSE for the user average rating prediction result.



# Compute average rating of each item and assign them to the predicted ratings of each user on the item.

## item 기준으로 평균 평점
itemAvgRatings = train[['movieId', 'rating']].groupby('movieId').agg('mean')
itemAvgRatings.columns = ['pred']
itemAvgRatings.head()
## 인기도 평균 평점

itemAvgPred = test[['userId', 'movieId', 'rating']]
itemAvgPred = pd.merge(itemAvgPred, itemAvgRatings, how='left', left_on=['movieId'], right_on=['movieId'], right_index = False)
itemAvgPred.head()

# Compute MAE and RMSE for the user average rating prediction result.

# +
itemAvgPredErrors = itemAvgPred['pred'] - itemAvgPred['rating']
mae3 = itemAvgPredErrors.abs().mean()
rmse3 = math.sqrt(itemAvgPredErrors.pow(2).mean())
print(mae3)
print(rmse3)

##item보다 user의 error 값이 더 낮음을 알 수 있음.
# -

# Read movie data and see the poster of movies.

dfMovie = pd.read_csv('movielens/movies_w_imgurl.csv')
dfMovie.head()

# +
from IPython.display import Image, display

for i in range(0, 5):
    display(Image(dfMovie['imgurl'].iloc[i]))
# -


