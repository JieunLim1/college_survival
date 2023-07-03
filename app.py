import streamlit as st
import time
import sqlite3 as sq3

# [TODO] GUI 형태로 만들어보기.
st.markdown("""# 대학생 구원자
---
- 이 앱은 학업에 지친 대학생에게 도움이 되고자 개발되어 필기한 내용들을 바탕으로 문제를 생성시켜 복습을 도와주는데 효율적입니다.
""")

context = st.text_area('여기에 문제를 생성할 원문을 적어주세요.')
#파일 받는 것도 만들어보기

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
# if 'q' not in st.session_state:
    
gen_button = st.button('문제 생성')
if gen_button:
    st.session_state['gen_button_clicked'] = True
    with st.spinner('Wait for it...'):
        st.session_state['q'] = q_engines[q_type](context) #객체 생성
#session_state는 파이썬의 딕셔너리 같은 형태로 저장

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
        if float(st.session_state['q'].jdata['Similarity']) > 0.8:
            st.balloons()
        st.write(result) #채점한 결과 띄우기
        st.session_state['q'].record(st.session_state['time']) # 데이터베이스에 삽입

    # record_button = st.button('기록보기')    
    # if record_button:
    #         con = sq3.connect("record1.db", isolation_level=None)
    #         cursor = con.cursor()
    #         cursor.execute('SELECT * FROM questions_data')
    #         rowList = cursor.fetchall()
    #         for row in rowList:
    #             st.write(row)
    #         cursor.close()

















