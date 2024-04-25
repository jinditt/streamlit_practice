import streamlit as st
import pandas as pd
import mysql.connector

conn= mysql.connector.connect(
    host= 'localhost',
    database = 'shopDB',
    user = 'streamlit',
    password = '1234'
)

if conn.is_connected():
    db_info = conn.get_server_info()
    st.write('server_version:', db_info)

cur = conn.cursor()
cur.execute('SELECT *FROM customer;')

# record = cur.fetchone()
# st.write('connected to DB: ', record)

records = cur.fetchall()
# st.write(records)

# @st.cache_data
def make_df():
    cur.execute('SELECT * FROM customer;')
    records = cur.fetchall()
    st.write(pd.DataFrame(records,
                      columns= ['id', 'name', 'phone', 'birth']))

# make_df() 이걸 왜 중간에 쓰셨는지는지 모르겠어요

with st.form(key='input_form'):
    id = st.number_input('고객번호', min_value=6)
    name = st.text_input('고객이름')
    phone = st.text_input('전화번호')
    birth = st.date_input('생년월일', value=None)
    submitted = st.form_submit_button('입력')

if submitted:
    sql = 'INSERT INTO customer (customer_id, customer_name, phone, birthday) values ('\
          + str(id) + ', \"' + name +'\" , \"' + phone + '\" , \"' + str(birth) + '\");'
    # sql로 위의 내용 확인 가능
    cur.execute(sql)
    conn.commit()
    make_df()
