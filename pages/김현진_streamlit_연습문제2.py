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

st.header('문제1')
st.subheader('1)')

iris = sns.load_dataset('iris')
iris_df = pd.DataFrame(iris)
st.write(iris_df)

st.subheader('2)')
st.write('multiselect를 사용하여 품종(species)을 선택하면, '
             '해당 품종의 데이터에 대한 데이터프레임으로 표시')
# 품종 선택
colors = st.multiselect('품종을 선택하세요',
                        options=['setosa', 'versicolor', 'virginica'])

# 선택한 품종에 해당하는 데이터프레임 생성
selected_df = iris[iris['species'].isin(colors)]
selected_df = iris[iris.species.isin(colors)]

# 선택한 품종 데이터프레임 출력
st.write(selected_df)

st.subheader('3)')
st.write('품종을 제외한 4가지 컬럼을 radio 요소를 사용하여 선택하면 '
         '선택한 컬럼에 대한 히스토그램 그리기(matplotlib)')
# 라디오 만들기
col = st.radio(
    label = '특징을 선택하세요',
    options = ['sepal_length', 'sepal_width', 'petal_length','petal_width'],
    captions=['잎의 길이', '잎의 너비', '꽃잎 길이', '꽃잎 너비'],
    horizontal=True)

# 선택한 컬럼으로 데이터프레임 생성
selected_data = iris[col]

# 그냥 pyplot 하면 경고가 뜸. 권장해 주는 방법으로 생성해보았으나 이유가 아직 이해 안 됨.
# 굳이 subplot을 써야 하나?
fig, ax = plt.subplots()
ax.hist(selected_data, bins=20)
ax.set_xlabel(col)
ax.set_ylabel('freq')
ax.set_title(f'{col}')

st.pyplot(fig)

#경고 받은 식
# plt.hist(selected_data, bins=20)
# plt.xlabel(col)
# plt.ylabel('빈도')
# plt.title(f'{col}의 분포')
#
#
# st.pyplot()

st.divider()

st.header('문제2')

# 문제점
#내림차순이 안 되는 이유를 알고 싶음.
#분류 선택 전에 ValueError가 안 떴으면 좋겠음

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
    ax.set_title('Top 20 Words Frequency')
    st.pyplot(fig)


sel_field = st.selectbox('대분류',
             [value for value in news['대분류'].unique()],
                     index=None,
                     placeholder='분야를 선택하세요')

df_sel_field = news[news['대분류']==sel_field]
sel_field_count = word_count(df_sel_field, '제목')
top_words(sel_field_count)



st.divider()

st.header('문제3')
# 위에서 발생한 선택 전에 valueError가 뜨는 문제를 해결하기 위해 버튼을 사용해보았으나 잠깐 뜨고 사라짐
st.write(''' 경기도인구데이터에 대하여 연도별 인구수에 대한 지도시각화
   2007년, 2015년, 2019년 연도를 탭으로 제시''')

import json

def show_population_map(year):
    # GeoJSON 파일 로드
    with open('data/경기도행정구역경계.json', encoding='utf-8') as f:
        geo_gg = json.loads(f.read())

    # 인구 데이터 로드
    df_gg = pd.read_excel('data/경기도인구데이터.xlsx', index_col='구분')

    # 지도 생성
    map = folium.Map(location=[37.5666, 126.9782], zoom_start=8)
    # 경기도 행정구역 경계 추가
    folium.GeoJson(geo_gg).add_to(map)

    # 인구 데이터에 대한 Choropleth 그래프 추가
    folium.Choropleth(geo_data=geo_gg,
                      data=df_gg[year],
                      columns=[df_gg.index, df_gg[year]],
                      key_on='feature.properties.name').add_to(map)

    # Streamlit 앱에 마크다운 표시
    st.markdown(f'{year}년 경기도 인구 데이터')

    # Streamlit 앱에 지도 추가
    st_folium(map, width=600, height=400)


selected_year = st.selectbox('연도 선택',
             [year for year in range(2007,2018)],
                     index=None,
                     placeholder='연도 선택')

if st.button('Show Map'):
    show_population_map(selected_year)

st.divider()

tab1, tab2, tab3 = st.tabs(['2007','2015','2017'])

with tab1:
    show_population_map(2007)
\
with tab2:
    show_population_map(2015)
with tab3:
    show_population_map(2017)