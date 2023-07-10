import streamlit as st
import time
import sqlite3 as sq3
import pandas as pd


# [TODO] GUI 형태로 만들어보기.
st.set_page_config(
    page_title="MAIN",
    page_icon="🧚🏻",
)
st.sidebar.success("Select a demo above.")

st.markdown("""# 대학생 구원자
---
- 이 앱은 학업에 지친 대학생에게 도움이 되고자 개발되어 필기한 내용들을 바탕으로 문제를 생성시켜 복습을 도와주는데 효율적입니다.
""")

con = sq3.connect("record1.db",isolation_level = None)
cursor = con.cursor()
cursor.execute("SELECT context FROM ctx_data")
row = cursor.fetchall() #[('',),('',) ...]
raw_data = [x[0][:80] for x in row]
print(row)
context = list(enumerate(raw_data,1)) #[(1,'...'),(...)]

option = st.selectbox('Which context would you like to select?', context)
st.write('You selected:', option)

if 'id' not in st.session_state:
    st.session_state['id'] = 0
if 'context' not in st.session_state:
    st.session_state['context'] = ''
st.session_state['id'] = option[0]
st.session_state['context'] = row[option[0]]


q_type = st.radio(
    "문제의 유형을 선택해주세요",
    ('FRQ', 'MCQ'))

st.divider() # 구분 짓는 선 긋기

from FRQ import FRQ
from MCQ import MCQ

q_engines = {
    'FRQ': FRQ,
    'MCQ': MCQ
    }

#session_state initialize
if 'gen_button_clicked' not in st.session_state:
    st.session_state['gen_button_clicked'] = False
    st.session_state['scoring_button_clicked'] = False
    st.session_state['recording_button_clicked'] = False
# if 'q' not in st.session_state:
    
gen_button = st.button('문제 생성')
if gen_button:
    st.session_state['gen_button_clicked'] = True
    with st.spinner('Wait for it...'):
        if 'q' not in st.session_state:
            st.session_state['q'] = q_engines[q_type](st.session_state['context']) #객체 생성

if st.session_state['gen_button_clicked']:
    question = st.session_state['q'].show_q()
    st.write(question) # 질문 띄우기

    st.session_state['user_answer'] = st.text_area("Enter your answer : ") #사용자로부터 입력값 받기
    scoring_button = st.button('채점 하기')
    if scoring_button:
        st.session_state['scoring_button_clicked'] = True
            
    if st.session_state['scoring_button_clicked']:
        now = time.localtime()
        now = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        st.session_state['time'] = now
        with st.spinner('Wait for it...'):
            result = st.session_state['q'].scoring(st.session_state['user_answer']) # 채점
        st.write(result) #채점한 결과 띄우기
        #st.session_state['q'].record(st.session_state['time']) # 데이터베이스에 삽입
        st.session_state['q'].qdata()
