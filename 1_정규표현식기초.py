# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + id="Ciu12CJ9CV8Z"
import re  # regular expression 정규표현식 라이브러리

# + id="WOH0ACiJCeDB"
text = 'abcaabbccaaabbbccc'

# + [markdown] id="tRnZ1H2o8YrB"
# ### 어떤 문자 한개 : .

# + colab={"base_uri": "https://localhost:8080/"} id="Lg8Lxji2Sov8" outputId="847b639e-af27-4ad7-aa32-827f7052585e"
print(re.findall('.', text))

## 어떤 문자 1개씩을 출력

# + colab={"base_uri": "https://localhost:8080/"} id="0C9N76bISl6f" outputId="73c586c3-d5cb-4237-afc3-2cebb66c52c6"
re.findall('a.', text)

## >ab  ca  >ab  bcc  >aa  >ab  bbccc
## a를 포함한 것을 출력

# + [markdown] id="UkHvLXJB8fYf"
# #### 0개 또는 1개 : ?

# + colab={"base_uri": "https://localhost:8080/"} id="MLn5duEGSj0W" outputId="26b1e350-0cde-485c-b188-f1af07bcf4ec"
print(re.findall('a?', text)) # a? = '', a

## a?는 a가 있거나 없거나를 1개씩 출력

# + [markdown] id="2G4Pv4NA8lAW"
# ### 0회 이상 : *
#

# + colab={"base_uri": "https://localhost:8080/"} id="qebdZyGmScHn" outputId="29f55214-9209-420c-f44c-78221a106129"
re.findall('a*', text) # a* = '', a, aa, aaa

## a가 0회 이상인 경우 출력

# + [markdown] id="H5cE5bth8pHo"
# ### 1회 이상 : +

# + colab={"base_uri": "https://localhost:8080/"} id="2RBvoOSASLbr" outputId="ec3ecf06-40ce-4382-81ae-fc186c9e2fc0"
re.findall('a+', text) # re.findall(<단어:정규표현식>, <문서>) / re.findall(<대상:정규표현식>, <위치>) 

## a가 1회 이상 등장하는 경우만 출력

# + id="7qXmwgFfDpOR"
doc = '''Ardino 23 010-1234-5678 onds@ardino.com
        Tom 21 016-345-6789 tom@ardino.com
        Jenny 25 011-123-5346 jny@ardino.com'''

# + [markdown] id="HWGUuwKh8s1X"
# ### 내가 원하는 것들 중 한개 : []

# + [markdown] id="AciBfNtL81n9"
# ### 내가 지정한 것들을 제외한 것들 중 한개 : [^]

# + [markdown] id="MaNRMY3Y87q3"
# ### 묶음, 묶은 것만 지칭 : ()

# + [markdown] id="RGXM41cl9GPA"
# ### 회피용법
# -

doc1 = 'TomCru'

# re.findall('[A-Za-z]+', doc1)
re.findall('[A-Z][A-Za-z]+', doc1)

# +
re.findall('A[a-z]+', doc)  ## A로 시작하고 뒤에 소문자 열[a-z]+로 끝나는 것을 출력

# re.findall('A[a-z]*', doc) ## +대신 *한 경우 A만 혼자 있는 경우도 찾게됨.
# -

re.findall('T[a-z]+', doc)

re.findall('J[a-z]+', doc)

re.findall('[A-Z][a-z]+', doc)

# + colab={"base_uri": "https://localhost:8080/"} id="sUiWEQvXEBAd" outputId="26ccacf1-8865-47d8-c218-3312e8874577"
# 이름들만 뽑기
# 알파벳대문자로 시작하고, 소문자들로 이어지는 
# 알파벳대문자 하나, 소문자 여러개
re.findall('[A-Z][a-z]+', doc)

# + colab={"base_uri": "https://localhost:8080/"} id="Lps_KMpSEKQx" outputId="9b2eaea9-04c8-4f5f-bd05-c07b69f2e37b"
# 나이만 뽑기
re.findall('\s([0-9][0-9])\s', doc) # 스페이스 사이에 있는 숫자2개
re.findall('[a-z]\s([0-9][0-9])', doc) # 소문자+스페이스 뒤에 숫자2개
re.findall('[A-Z][a-z]+\s(..)', doc) # 이름+스페이스 뒤에 어떤문자2개
re.findall('[A-Z][a-z]+\s(.+?)\s', doc) # 이름+스페이스와 스페이스 사이의 (최대한짧은) 어떤문자열

# + colab={"base_uri": "https://localhost:8080/"} id="pubvmAIcELtj" outputId="aa56fae2-799f-4539-f48f-4984e844b812"
# 전화번호만 뽑기
re.findall('[0-9\-]+', doc) # [] 안에서는 or로 연결되기때문에, 숫자로만 이루어진 문자열도 같이 뽑힘
re.findall('[0-9]+\-[0-9]+\-[0-9]+', doc)

# + colab={"base_uri": "https://localhost:8080/"} id="LUN5IVmhENx5" outputId="ea040f02-37c6-4952-b272-f3c24f3f5b63"
# 이메일만 뽑기
re.findall('[a-z]+@[a-z]+\.[a-z]+', doc)

# + [markdown] id="18f-Nfrb9JBf"
# ### Greedy Q : .+ / Reluctant Q : .+?

# + id="MRpjVDo-SqZ8"
text = 'ardino is not altino'

# + colab={"base_uri": "https://localhost:8080/"} id="gEXnl6Kd8WGa" outputId="c25d3adb-2b8d-45fe-a74f-ff4fd4d28870"
re.findall('a.+o', text)

# + colab={"base_uri": "https://localhost:8080/"} id="Hq66mQG09Tco" outputId="c6cf8188-f6a5-4e5d-8ded-408deea86f8c"
re.findall('a.+?o', text)

# + [markdown] id="gMVEosiZ9a2n"
# ### 연습 : 타이타닉 데이터 이름 컬럼에서 middle name만 추출하기

# + colab={"base_uri": "https://localhost:8080/", "height": 200} id="73OgqEM9WMc2" outputId="556b5454-a299-4dbb-d480-b65c27472405"
import pandas as pd

df_titanic = pd.read_csv("https://raw.githubusercontent.com/datascienceschool/docker_rpython/master/data/titanic.csv")
df_titanic.head()

# + colab={"base_uri": "https://localhost:8080/"} id="gAtdNx0f9sW4" outputId="80e1dd2d-cbb0-4bd5-e416-317f985e0f6c"
name1 = df_titanic[['Name']].iloc[0] # first person name
name1

# + colab={"base_uri": "https://localhost:8080/"} id="TjIwhsJ4bwgw" outputId="cfe95fe3-d9ed-47b6-e611-1c0eb8b2832f"
re.findall('\s([A-Za-z]+)\.', str(name1))

# + id="rIw_FPHbftDn" colab={"base_uri": "https://localhost:8080/", "height": 411} outputId="1a0822a2-1584-4f20-bf62-843cf6dbedaa"
# 한 컬럼 전체에 모두 동일한 문자열 관련 기능을 적용하는 방법
df_titanic['Name'].str.extract('\s([A-Za-z]+)\.')
# -




