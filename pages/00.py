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

plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':  # 맥OS
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # 윈도우
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system...  sorry~~~')


st.header('문제2')
st.write('''kor_news 데이터셋을 이용.  
분류의 대분류 기준을 선택하면 해당 분야의 주요 키워드 20위에 대한 bar chart 표시''')
news = pd.read_excel('data/kor_news_240326.xlsx')
news['분류리스트'] = news.분류.str.split('>')
news['대분류'] = news.분류리스트.str[0]
news['중분류'] = news.분류리스트.str[1]
news['소분류'] = news.분류리스트.str[2]


def word_count(df, column_name):
    cont = list(df[column_name])
    okt = Okt()
    token_tags = [okt.pos(word) for word in cont]
    token_list = []
    for token_tag in token_tags:
        result = []
        for token, tag in token_tag:
            if (len(token) > 1) and (tag == 'Noun'):
                result.append(token)
        token_list.append(result)
    tokens = np.hstack(token_list)
    count = Counter(tokens)
    df = pd.DataFrame(pd.Series(count), columns=['Freq'])
    df = df.sort_values(by='Freq', ascending=False)
    return df

def top_words(df):
    df = df.iloc[:20].sort_values(by='Freq', ascending=False)
    fig, ax = plt.subplots()
    ax.barh(df.index, df['Freq'])
    ax.set_xlabel('Freq')
    ax.set_ylabel('Word')
    ax.set_title(f'Top 20 Words Frequency')
    st.pyplot(fig)


sel_field = st.selectbox('대분류',
             [value for value in news['대분류'].unique()],
                     index=None,
                     placeholder='분야를 선택하세요')

df_sel_field = news[news['대분류']==sel_field]
sel_field_count = word_count(df_sel_field, '제목')
top_words(sel_field_count)

# 내림차순이 안 되는 이유를 알고 싶음.
# 분류 선택 전에 Value Error가 안 떴으면 좋겠음





