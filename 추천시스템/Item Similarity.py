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

# # Example Items
# These are sample items we are going to handle in this exercise.

# ![](image1.png)

# Import necessary packages for the exercise.

# + jupyter={"outputs_hidden": true}
import math
import numpy as np
# -

# # Item Similarity

# ### Weight Matrix
# Create a binary valued matrix that holds the item's genre accurance in each cell.

# +
## CBF 평점 예측 
## 장르에 대한 벡터 표현
matrix = np.array(
    [
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0, 0]
    ]
)

print("Items : ", matrix.shape[0])
print("Genres: ", matrix.shape[1])
## item 11, 장르 8
# -

# Create a matrix that will hold weights for all items.
#
# We will compute weights by TF-IDF scheme.
# * We will use 1 for TF of each genre in items.
# * We will compute IDFs for genres and assign them in column-wise manner.

# + jupyter={"outputs_hidden": true}
totalItems = matrix.shape[0]
totalGenres = matrix.shape[1]

## 0 채워진 shape를 만듬
weights = np.zeros(matrix.shape)

for i in range(0, totalGenres): ## 전체 장르 0부터 8까지 계산을함
    col = matrix[:,i]          ## columns을 가져옴
    df = col.sum()             ##   col을 계산
    idf = math.log10(totalItems/df)  ## idf 값 계산
    for j in range(0, totalItems):   ## 컬럼 별로 해당하는 item들에 대해서 계산
        weights[j, i] = matrix[j, i] * idf ## j번째 item에 i번째 장르에 대한 w는 matrix j,i(TF)*IDF 
# -

# See the weights.

weights


# ### $l_2$-norm
# Let's define norm2 function for computing l2-norm of a vector, which is represented as an array in np.
#
# $$norm2(v)=||v||_2=\sqrt{\sum_{\forall i}v_i^2}$$

# + jupyter={"outputs_hidden": true}
def norm2(arr):
    sum = 0.0
    for i in range(0, len(arr)):
        sum += arr[i] * arr[i]
    return math.sqrt(sum)


# -

print(weights[0], "=>", norm2(weights[0]))
print(weights[1], "=>", norm2(weights[1]))


# ### Inner Product
#
# Let's define dot function for computin inner product between two vectors.
#
# $$dot(u, v)=u\cdot v=\sum_{\forall i}{u_i \times v_i}$$

# + jupyter={"outputs_hidden": true}
def dot(arr1, arr2):
    sum = 0.0
    for i in range(0, len(arr1)):
        sum += arr1[i] * arr2[i]
    return sum


# -

print(dot(weights[0], weights[1]))
print(dot(weights[0], weights[2]))
print(dot(weights[0], weights[3]))


# ### Cosine Similarity
#
# Let's define cosine similarity function for two vectors.
#
# $$ cosine(u, v)=\frac{dot(u,v)}{norm2(u)norm2(v)}=\frac{u\cdot v}{||u||_2||v||_2} $$

# + jupyter={"outputs_hidden": true}
def cosine(arr1, arr2): # 두개의 arr를 받음
    return dot(arr1, arr2)/(norm2(arr1)*norm2(arr2)) 


# -

print(cosine(weights[0], weights[1]))
print(cosine(weights[0], weights[2]))
print(cosine(weights[0], weights[3]))

# # Easy Computation using `numpy`
# Let's do this in a more convenient way with *numpy's linalg*

# + jupyter={"outputs_hidden": true}
from numpy import linalg as LA
# -

# Compute norms and save it to **`norms`**.

## numpy의 norm을 사용해서 계산, ord 2로 하여 계산
norms = LA.norm(weights, ord=2, axis=1)
norms

# Compute inner products among all items. 

## matmul로 계산
dots = np.matmul(weights, weights.T)
dots

## divide 
## 각행이 norms으로 나눠짐, 방향에 대해서 첫번째 벡터나누고 두번째 벡터로 나누는 처리 .T 하고 norms로 나눠줌
sims = np.divide(np.divide(dots, norms).T, norms)
sims

## 첫번째 벡터와 유사도
sims[0]


