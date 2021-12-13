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

# # Best Recommendation

# 확장 기능 로드 및 데이터 베이스 초기화

# +
# %reload_ext sql
# %run lib.py

# %sql postgresql+psycopg2://postgres:@127.0.0.1:5432/fcrec
# -

# # Best Products from Click Log

# Create click best table

# + language="sql"
# drop table if exists cmc_product_click_best;
#
# create table cmc_product_click_best as
# select t.item_no, t.score, row_number() over (order by score desc) rank
# from ( 
# 	select item_no, count(distinct session_id) score
# 	from cmc_event a
# 	where event_name = 'click_item'
# 		and a.event_timestamp between '2021-07-18' and '2021-07-25'
# 	group by a.item_no 
# 	) t
# order by score desc;
# -

# Check click best items

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_product_click_best a
        join cmc_product b on a.item_no = b.item_no
    order by score desc
    limit 10
    '''

result1 = executeQuery(query) 
displayItemInRows(result1) # 클릭이 많이된 실제 이미 출력
# -

# # Best Products from Purchase Log

# Create purchase best table

# + language="sql"
# drop table if exists cmc_product_purchase_best;
#
#
# create table cmc_product_purchase_best as
# select t.item_no, t.score, row_number() over (order by score desc) rank
# from ( 
# 	select a.item_no, sum(log(b.price::float + 1)::int) score
# 	from cmc_event a 
# 		join cmc_product b on b.item_no = a.item_no
# 	where a.event_name = 'purchase_success'
# 		and a.event_timestamp between '2021-07-18' and '2021-07-25'
# 	group by a.item_no
# 	) t
# order by score desc;
# -

# Check purchase best items

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_product_purchase_best a
        join cmc_product b on a.item_no = b.item_no
    order by score desc
    limit 10
    '''

result2 = executeQuery(query)
displayItemInRows(result2)
# -

# # Best Products from Purchase and Click Log

# Scoring with  w1 * view + w2 * order

# + language="sql"
# drop table if exists cmc_product_best;
#
# create table cmc_product_best as
# select t.item_no, t.score, row_number() over (order by score desc) rank
# from ( 
# 	select item_no, sum(score) score
# 	from (
# 		select item_no, score
# 		from cmc_product_click_best
# 		union all
# 		select item_no, score * 3
# 		from cmc_product_purchase_best ) t
# 	group by item_no
# 	) t
# order by score desc;

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_product_best a
        join cmc_product b on a.item_no = b.item_no
    order by score desc
    limit 10
    '''

result3 = executeQuery(query)
displayItemInRows(result3)
# -

# # Comparison of Best Products

displayItemInRows(result1)
displayItemInRows(result2)
displayItemInRows(result3)

# # Category 1 Best Products

# + language="sql"
# drop table if exists cmc_category1_best;
#
# create table cmc_category1_best as
# select b.category1_code, b.item_no, a.score, row_number() over (partition by b.category1_code order by a.score desc) rank
# from cmc_product_best a
# 	join cmc_product b on b.item_no = a.item_no

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_category1_best a
        join cmc_product b on a.item_no = b.item_no
    where a.category1_code = '243100100'
    order by score desc
    limit 10
    '''

result4 = executeQuery(query)
displayItemInRows(result4)

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_category1_best a
        join cmc_product b on a.item_no = b.item_no
    where a.category1_code = '244100100'
    order by score desc
    limit 10
    '''

result5 = executeQuery(query)
displayItemInRows(result5)

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_category1_best a
        join cmc_product b on a.item_no = b.item_no
    where a.category1_code = '248100100'
    order by score desc
    limit 10
    '''

result6 = executeQuery(query)
displayItemInRows(result6)
# -

# # Category 2 Best Products

# + language="sql"
# drop table if exists cmc_category2_best;
#
# create table cmc_category2_best as
# select b.category2_code, b.item_no, a.score, row_number() over (partition by b.category2_code order by a.score desc) rank
# from cmc_product_best a
# 	join cmc_product b on b.item_no = a.item_no;
# -

# ## Category 2 Best Example (상의)

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_category2_best a
        join cmc_product b on a.item_no = b.item_no
    where a.category2_code = '243102100'
    order by score desc
    limit 10
    '''

result7 = executeQuery(query)
displayItemInRows(result7)
# -

# ## Category 2 Best Example (하의)

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_category2_best a
        join cmc_product b on a.item_no = b.item_no
    where a.category2_code = '243104100'
    order by score desc
    limit 10
    '''

result8 = executeQuery(query)
displayItemInRows(result8)
# -

# # Gender Best

# + language="sql"
#
# drop table if exists cmc_product_gender_best;

# + language="sql"
#
# drop table if exists cmc_product_gender_best;
#
# create table cmc_product_gender_best as
# with click_best as (
# 	select b.gender, item_no, count(distinct session_id) score
# 	from cmc_event a join cmc_user b on b.user_no = a.user_no
# 	where event_name = 'click_item'
# 		and a.event_timestamp between '2021-07-18' and '2021-07-25'
# 	group by b.gender, a.item_no),
# 	purchase_best as (
# 	select c.gender, a.item_no, sum(log(b.price::float + 1)::int) score
# 	from cmc_event a 
# 		join cmc_product b on b.item_no = a.item_no
# 		join cmc_user c on c.user_no = a.user_no
# 	where a.event_name = 'purchase_success'
#         and a.event_timestamp between '2021-07-18' and '2021-07-25'
# 	group by c.gender, a.item_no )
# select t.gender, t.item_no, t.score, row_number() over (order by score desc) rank
# from ( 
# 	select gender, item_no, sum(score) score
# 	from (
# 		select gender, item_no, score
# 		from click_best
# 		union all
# 		select gender, item_no, score * 3
# 		from purchase_best ) t
# 	group by gender, item_no
# 	) t
# order by gender, score desc;
# -

# ## Female Best

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_product_gender_best a
        join cmc_product b on a.item_no = b.item_no
    where a.gender = 'F'
    order by score desc
    limit 10
    '''

result9 = executeQuery(query)
displayItemInRows(result9)
# -

# ## Male Best

# +
query = '''
    select a.rank, a.score, b.*
    from cmc_product_gender_best a
        join cmc_product b on a.item_no = b.item_no
    where a.gender = 'M'
    order by score desc
    limit 10
    '''

result10 = executeQuery(query)
displayItemInRows(result10)
