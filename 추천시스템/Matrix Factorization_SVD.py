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

# # Matrix Factorization: SVD

# +
# %run liblecture.py

from numpy import linalg as LA
from scipy.sparse import coo_matrix
from scipy.linalg import sqrtm

# -

# ## Read Data: movies and ratings
# Read Movies and Define displayMovies

movies = pd.read_csv('movielens/movies_w_imgurl.csv')
movies

# Read Rating Data

ratings

# +
ratings = pd.read_csv('ratings-9_1.csv')

## type을 통해 9:1 분리
train = ratings[ratings['type'] == 'train'][['userId', 'movieId', 'rating']]
test = ratings[ratings['type'] == 'test'][['userId', 'movieId', 'rating']]
# -

# ## Convert Ratings to User-Item Sparse Matrix
# ### Create Index to Id Maps

# +
movieIds = train.movieId.unique()

movieIdToIndex = {}
indexToMovieId = {}

colIdx = 0

for movieId in movieIds:
    movieIdToIndex[movieId] = colIdx
    indexToMovieId[colIdx] = movieId
    colIdx += 1
movieIds 
## movieIds matrix

# +
userIds = train.userId.unique()

userIdToIndex = {}
indexToUserId = {}

rowIdx = 0

for userId in userIds:
    userIdToIndex[userId] = rowIdx
    indexToUserId[rowIdx] = userId
    rowIdx += 1
userIds 
## user matrix
# -

# ### Creat User-Item Sparse Matrix

# +
rows = []
cols = []
vals = []

for row in train.itertuples():
    rows.append(userIdToIndex[row.userId])
    cols.append(movieIdToIndex[row.movieId])
    vals.append(row.rating)

coomat = coo_matrix((vals, (rows, cols)), shape=(rowIdx, colIdx))

matrix = coomat.todense()
matrix.shape
## sparse matrix
# -

# ## Sigular Value Decomposition

# +
## np에 LA.svd를 사용해서 coordinate matrix = coomat 를 전달함 / full_matrices = False로 해서 tuple 반환
U, s, V = LA.svd(coomat.toarray(), full_matrices = False)
U


# -

# ### Define user and item feautre matrix

U.shape

# 50 차원
dim = 100
sqrtS = sqrtm(np.diag(s[0:dim]))

userFeatures = np.matmul(U.compress(np.ones(dim), axis=1), sqrtS)
itemFeatures = np.matmul(V.T.compress(np.ones(dim), axis=1), sqrtS.T)

userFeatures.shape
# 50 dim 으로 축소 확인

itemFeatures.shape
# 50 dim 으로 축소 확인

# ### Compute item similarity matrixes

## itemFeatures norm 값 구하기.
itemNorms = LA.norm(itemFeatures, ord = 2, axis=1)
normalizedItemFeatures = np.divide(itemFeatures.T, itemNorms).T
itemSims = pd.DataFrame(data = np.matmul(normalizedItemFeatures, normalizedItemFeatures.T), index = movieIds, columns=movieIds)
itemSims
## 유사도 계산

# ### Check Example 

# +
movieIdx = 6

rels = itemSims.iloc[movieIdx,:].sort_values(ascending=False).head(6)[1:]

displayMovies(movies, [indexToMovieId[movieIdx]])
displayMovies(movies, rels.index, rels.values)
# -

# ## User Rating Prediction

# +
userId = 10

userRatings = train[train['userId'] == userId][['movieId', 'rating']] 

userRatings
# -

# ### Predict Ratings

# +
recSimSums = itemSims.loc[userRatings['movieId'].values, :].sum().values

recWeightedRatingSums = np.matmul(itemSims.loc[userRatings['movieId'].values, :].T.values, userRatings['rating'].values)

recItemRatings = pd.DataFrame(data = np.divide(recWeightedRatingSums, recSimSums), index=itemSims.index)

recItemRatings.columns = ['pred']

recItemRatings
# -

# ### Compute Errors (MAE, RMSE)

# +
userTestRatings = pd.DataFrame(data=test[test['userId'] == userId])

temp = userTestRatings.join(recItemRatings.loc[userTestRatings['movieId']], on='movieId')

mae = getMAE(temp['rating'], temp['pred'])
rmse = getRMSE(temp['rating'], temp['pred'])

print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
# -

# ### Compare Logs and Recommendations

# +
logs = userRatings.sort_values(by='rating', ascending=False).head(20)
recs = recItemRatings.sort_values(by='pred', ascending=False).head(20)

print("logs")
displayMovies(movies, logs['movieId'].values, logs['rating'].values)

print("recs")
displayMovies(movies, recs.index, recs['pred'].values)
# 

