import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from konlpy.tag import Okt
from collections import Counter
import platform
from matplotlib import font_manager, rc

def preprocess(df):
    df['분류리스트'] = df.분류.str.split('>')
    df['대분류'] = df['분류리스트'].str[0]

@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    return preprocess(df)

news = pd.read_excel('data/kor_news_240326.xlsx')
st.dataframe(news)

st.subheader('2. URL column configuration')
st.data_editor(news,
               column_config={
                   'URL':st.column_config.LinkColumn(
                       help='기사 링크',
                       max_chars= 200
                   )
               })

st.subheader('3. 대분류 컬럼에 대한 빈도 bar chart')

df = pd.DataFrame(news.대분류.value_counts())
st.bar_chart(df)


st.subheader('''4. 제목 컬럼 주요 키워드 20위''')
def word_counts(df, column_name):
    text = list(df[column_name])
    okt = Okt()
    token_pos = [okt.pos(word) for word in text]

    token_list = []
    for token_tag in token_pos:
        result = []
        for token, tag in token_tag:
