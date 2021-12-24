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

# # Related Products Recommendation

# 확장 기능 로드 및 데이터베이스 접속

# +
# %reload_ext sql
# %run lib.py

# %sql postgresql+psycopg2://postgres:@127.0.0.1:5432/fcrec
# -

# # Related Products based on User Occurrence

# + language="sql"
# drop table if exists cmc_user_product_click_cnt;

# + language="sql"
# drop table if exists cmc_user_product_click_cnt;
#
# create table cmc_user_product_click_cnt as
# select user_no, item_no, count(*) cnt
# from cmc_event a
# where event_name = 'click_item'
# 	and a.event_timestamp between '2021-07-18' and '2021-07-25'
# group by user_no, item_no;
# -

# ## 클릭 횟수 분포 확인

# +
query = '''
    select cnt, count(*)
    from cmc_user_product_click_cnt
    group by cnt;
    '''

res1 = executeQuery(query)
# -

import matplotlib.pyplot as plt 
## 이걸 세팅해주세요. 
plt.style.use(['dark_background'])

# +
import pandas as pd

df = pd.DataFrame(res1, columns=['cnt', 'count'])
df.plot.bar(x='cnt', y='count', rot=0, figsize=(20,5))

# -

# ## Create user product click weight table (normalized)

# + language="sql"
# drop table if exists cmc_user_product_click_w;

# + language="sql"
# drop table if exists cmc_user_product_click_w;
#
# create table cmc_user_product_click_w as
# select user_no, item_no, w/sqrt(sum(w*w) over (partition by user_no)) w
# from (
# 	select user_no, item_no, (ln(cnt)+1) w
# 	from cmc_user_product_click_cnt ) t;
#
# create index idx_cmc_user_product_click_w_1 on cmc_user_product_click_w (user_no, item_no, w);
#
# create index idx_cmc_user_product_click_w_2 on cmc_user_product_click_w (item_no, user_no, w);
# -

# ### Get related products of '6tt2Q2Jveb2qyFrH78Fwqw=='

# +
item_no = '6tt2Q2Jveb2qyFrH78Fwqw=='

# result = %sql select * from cmc_product where item_no = :item_no;

query1 = f'''
    with cmc_product_sim as (
        select b.item_no, count(*) sim -- sum(a.w * b.w) sim
        from cmc_user_product_click_w a 
            join cmc_user_product_click_w b on a.user_no = b.user_no and a.item_no != b.item_no
        where a.item_no = '{item_no}'
        group by b.item_no
        order by sim desc
        limit 20)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    '''
result1 = executeQuery(query1)

query2 = '''
    with cmc_product_sim as (
        select b.item_no, sum(a.w * b.w) sim
        from cmc_user_product_click_w a 
            join cmc_user_product_click_w b on a.user_no = b.user_no and a.item_no != b.item_no
        where a.item_no = '{item_no}'
        group by b.item_no
        order by sim desc
        limit 20)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    '''
result2 = executeQuery(query2)

displayItemInRows(result)
displayItemInRows(result1)
displayItemInRows(result2)
# -

# # Related Products based on Session Occurrence

# + language="sql"
# drop table if exists cmc_session_product_click_cnt;
#
# create table cmc_session_product_click_cnt as
# select session_id, item_no, count(*) cnt
# from cmc_event a
# where event_name = 'click_item'
# 	and a.event_timestamp between '2021-07-18' and '2021-07-25'
# group by session_id, item_no;
# -

# 클릭 횟수 분포 확인

# +
query = '''
    select cnt, count(*)
    from cmc_session_product_click_cnt
    group by cnt;
    '''

res1 = executeQuery(query)

df = pd.DataFrame(res1, columns=['cnt', 'count'])
df.plot.bar(x='cnt', y='count', rot=0, figsize=(20,5))
# -

# ## Create session product click weight table (normalized)

# + language="sql"
# drop table if exists cmc_session_product_click_w;
#
# create table cmc_session_product_click_w as
# select session_id, item_no, w/sqrt(sum(w*w) over (partition by session_id)) w
# from (
# 	select session_id, item_no, (ln(cnt)+1) w
# 	from cmc_session_product_click_cnt ) t;
#
# create index idx_cmc_session_product_click_w_1 on cmc_session_product_click_w (session_id, item_no, w);
#
# create index idx_cmc_session_product_click_w_2 on cmc_session_product_click_w (item_no, session_id, w);
# -

# ### Get related products of '6tt2Q2Jveb2qyFrH78Fwqw=='

# +
item_no = '6tt2Q2Jveb2qyFrH78Fwqw=='

# result = %sql select * from cmc_product where item_no = :item_no;

query3 = f'''
    with cmc_product_sim as (
        select b.item_no, count(*) sim -- sum(a.w * b.w) sim
        from cmc_session_product_click_w a 
            join cmc_session_product_click_w b on a.session_id = b.session_id and a.item_no != b.item_no
        where a.item_no = '6tt2Q2Jveb2qyFrH78Fwqw=='
        group by b.item_no
        order by sim desc
        limit 20)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    '''
result3 = executeQuery(query3)

query4 = f'''
    with cmc_product_sim as (
        select b.item_no, sum(a.w * b.w) sim
        from cmc_session_product_click_w a 
            join cmc_session_product_click_w b on a.session_id = b.session_id and a.item_no != b.item_no
        where a.item_no = '6tt2Q2Jveb2qyFrH78Fwqw=='
        group by b.item_no
        order by sim desc
        limit 20)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    '''
result4 = executeQuery(query4)

displayItemInRows(result)
displayItemInRows(result3)
displayItemInRows(result4)
# -

# ## Consider Popularity

# + language="sql"
#
# drop table if exists cmc_session_product_click_w2;
#
# create table cmc_session_product_click_w2 as
# with df as (
# 	select session_id, count(*) df
# 	from cmc_session_product_click_cnt 
# 	group by session_id )
# select session_id, item_no, w/sqrt(sum(w*w) over (partition by session_id)) w
# from (
# 	select a.session_id, a.item_no, (ln(cnt)+1)*ln(100200.0/df + 1.0) w
# 	from cmc_session_product_click_cnt a left join df b on a.session_id = b.session_id
# ) t;
#
#
# create index idx_cmc_session_product_click_w2_1 on cmc_session_product_click_w2 (session_id, item_no, w);
#
# create index idx_cmc_session_product_click_w2_2 on cmc_session_product_click_w2 (item_no, session_id, w);

# +
query5 = f'''
    with cmc_product_sim as (
        select b.item_no, sum(a.w * b.w) sim
        from cmc_session_product_click_w2 a 
            join cmc_session_product_click_w2 b on a.session_id = b.session_id and a.item_no != b.item_no
        where a.item_no = '{item_no}'
        group by b.item_no
        order by sim desc
        limit 20)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    '''
result5 = executeQuery(query5)

displayItemInRows(result)
displayItemInRows(result3)
displayItemInRows(result4)
displayItemInRows(result5)
# -

# ## 대체재

# +
query6 = f'''
    with cmc_product_sim as (
        select b.item_no, sum(a.w * b.w) sim
        from cmc_session_product_click_w2 a 
            join cmc_session_product_click_w2 b on a.session_id = b.session_id and a.item_no != b.item_no
        where a.item_no = '{item_no}'
        group by b.item_no
        order by sim desc)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    where b.category3_code = (select category3_code from cmc_product where item_no = '{item_no}')
    order by a.sim desc
    limit 20
    '''
result6 = executeQuery(query6)

displayItemInRows(result)
displayItemInRows(result6)
# -

# ## 보완재

# +
query7 = f'''
    with cmc_product_sim as (
        select b.item_no, sum(a.w * b.w) sim
        from cmc_session_product_click_w2 a 
            join cmc_session_product_click_w2 b on a.session_id = b.session_id and a.item_no != b.item_no
        where a.item_no = '{item_no}'
        group by b.item_no
        order by sim desc)
    select a.sim, b.*
    from cmc_product_sim a 
        join cmc_product b on b.item_no = a.item_no
    where b.category2_code != (select category2_code from cmc_product where item_no = '{item_no}')
    order by a.sim desc
    limit 20
    '''
result7 = executeQuery(query7)

displayItemInRows(result)
displayItemInRows(result7)
# -


