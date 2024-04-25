import json
import pandas as pd
import os
import streamlit as st
import folium

@st.cache_data

이런 식으로 만들어 놓고 나서 다른 곳에서 활용할 때,
아래처럼 쓰고 난 뒤에 함수 사용하면 됨.


from utils.map import load_data, load_geo_json, load_excel_data
from utils.map import load_data, load_geo_json, load_excel_data

