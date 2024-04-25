import pandas as pd
import numpy as np
import streamlit as st
import time

st.subheader('Data Column Config')
st.subheader('1. Column')
df = pd.DataFrame(
    [{'command': 'st.write','rating':4, 'is_widget':False},
    {'command': 'st.dataframe', 'rating': 5, 'is_widget': True},
    {'command': 'st.time_input', 'rating': 3, 'is_widget': True},
    {'command': 'st.metric', 'rating': 4, 'is_widget': True}])

st.dataframe(df)
st.markdown('column(label=, help=, width=)')
st.dataframe(df,
             column_config={
                 'command': st.column_config.Column(
                     label='Streamlit Commands',
                     help= 'Streamlit **widget** commands',
                     width='medium'
                 )
             })

st.markdown('column(label=, help=, width=, disabled=)')
st.data_editor(df,
               column_config={
                 'command': st.column_config.Column(
                     label='Streamlit Commands',
                     help= 'Streamlit **widget** commands',
                     width='medium',
                     disabled=True
                 )
             })
st.subheader('2. Text Column')
# st.dataframe(df)
st.markdown('text_column(default=)')
st.data_editor(df,
               column_config={
                 'command': st.column_config.TextColumn(
                     label='Streamlit Commands',
                     help= 'Streamlit **widget** commands',
                     default='st.',
                 )
             },
             num_rows='dynamic')

st.markdown('text_column(validate=)')
st.data_editor(df,
               column_config={
                 'command': st.column_config.TextColumn(
                     label='Streamlit Commands',
                     help= 'Streamlit **widget** commands',
                     default='st.',
                     max_chars=15,
                     validate='^st\.[a-z_]+$' #$가 0개 이상을 뜻하는 건가
                 )},
             num_rows='dynamic')

st.subheader('3. Number Column')
st.data_editor(df,
               column_config={
                   'rating':st.column_config.NumberColumn(
                       label='좋아요',
                       help='한 달 동안의 좋아요 수',
                       min_value=0,
                       max_value=10,
                       step=0.5,
                       format='$%f' # d면 정수값
                   )
               })
st.subheader('4. Checkbox Column')
st.data_editor(df,
               column_config={
                   'is_widget': st.column_config.CheckboxColumn(
                       label='위젯인가?',
                       default= False),

                   'command': st.column_config.TextColumn(
                     label='Streamlit Commands',
                     help= 'Streamlit **widget** commands',
                     default='st.',
                     max_chars=15,
                     validate='^st\.[a-z_]+$')
               },
               num_rows='dynamic')

st.subheader('5. Selectbox Column')
df2 = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)

st.data_editor(df2)

st.data_editor(
    df2,
    column_config={
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
            ],
            required=True,
        )
    },
    hide_index=True,
)

from datetime import datetime, date, time
st.subheader('6. Datetime Column')
df3 = pd.DataFrame(
    {'meeting_date':
     [datetime(2024,2,5,12,30),
      datetime(2024,2,7,2,30),
      datetime(2024,3,5,10,30),
      datetime(2024,6,15,11,00),
      datetime(2024,9,2,12,30)
      ]}
)

st.data_editor(df3)

st.data_editor(df3,
               column_config={
                'meeting_date': st.column_config.DatetimeColumn(
                    min_value=datetime(2024,1,1),
                    max_value=datetime(2024,4,30),
                    format= 'D MMM YYYY, h:mm a'
                )
               })

st.subheader('7. Date Column')
df4 = pd.DataFrame(
    {'meeting_date':
     [datetime(2024,2,5),
      datetime(2024,2,7),
      datetime(2024,3,5),
      datetime(2024,6,15),
      datetime(2024,9,2)
      ]}
)

st.dataframe(df4)
st.data_editor(df4,
               column_config={
                   'meeting_date': st.column_config.DateColumn(
                       min_value=date(2023,1,1),
                       max_value=date(2025,12,31),
                       format='YYYY/MM/DD'
               )})

st.subheader('8. Time Column')
df5 = pd.DataFrame(
    {'meeting_date':
     [time(12,30),
      time(3,5), # 05라고 하면 앙댐
      time(5,23),
      time(9,17),
      time(10,00),
      ]}
)

st.data_editor(df5,
               column_config={
                   'meeting_time': st.column_config.TimeColumn(
                       min_value=time(9,0,0),
                       max_value=time(18,0,0),
                       format='hh:mm a'
               )})

st.subheader('9. List Column')
df6 = pd.DataFrame(
    {
        'score' : [[0,4,60,80,100],
                   [90,98,88,60,56],
                   [88,92,68,74,20]]
    }
)

st.dataframe(df6)
st.data_editor(df6, # 내용 수정 불가.
             column_config={
                 'score': st.column_config.ListColumn(
                     width='medium'
                 )
             })
st.table(df6)

st.subheader('10.Link Column')
df7 = pd.DataFrame(
    {
        'site': ['naver', 'daum', 'google'],
        'url': ['https://www.naver.com/',
                'https://www.daum.net/',
                'https://www.google.com/']
    }
)


st.dataframe(df7)
st.data_editor(df7,
             column_config={
                 'url' : st.column_config.LinkColumn(
                     help = 'Search portal site!',
                     max_chars=100,
                     validate='^https://www\.[a-z]+\.[a-z]+',
                     display_text='Search site'
                 )
             })

st.subheader('11. Chart Column')
df8 = pd.DataFrame(
    {
        'name' : ['Kim', 'Lee', 'Choi'],
        'score' : [[0,4,60,80,100],
                   [90,98,88,60,56],
                   [88,92,68,74,20]
        ],
        'score2' : [[0,4,60,80,100],
                   [90,98,88,60,56],
                   [88,92,68,74,20]],

        'score3': [[0, 4, 60, 80, 100],
                   [90, 98, 88, 60, 56],
                   [88, 92, 68, 74, 20]]
    })

st.dataframe(df8,
              column_config={
                  'score2': st.column_config.LineChartColumn(
                      y_min=0, y_max=100
                  ),
                  'score3': st.column_config.AreaChartColumn(
                      y_min=0, y_max=100
                  ),
                  'score' : st.column_config.BarChartColumn(
                      y_min=0, y_max=100
                  )
              })

st.subheader('12. Image Column')
df9 = pd.DataFrame({
    "image": [
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/ef9a7627-13f2-47e5-8f65-3f69bb38a5c2/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/31b99099-8eae-4ff8-aa89-042895ed3843/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png",
        ]
    # 'png_image':[
    #     'img/apple.png',
    #     'img/banana.png'
    #     'img/mango.png'
    })

st.dataframe(df9,
             column_config={
                 'image':st.column_config.ImageColumn()
             })

st.subheader('13. Progress Column')
df10 = pd.DataFrame({'sales': [100,50,60,70]})

st.data_editor(df10,
               column_config={
                   'sales': st.column_config.ProgressColumn(
                       # min_value=0, max_value=150,
                       # format='%f조'
                   )
               })