import streamlit as st
import sqlite3 as sq3
import pandas as pd



st.set_page_config(page_title="Generating Your Exam Paper", page_icon="📝")
st.markdown(""" # Examination Paper 
----
Create Your Test Paper""")
q_number = st.text_input("몇개의 질문을 생성하시겠습니까?")
q_number = int(q_number)

con = sq3.connect("record1.db", isolation_level = None)
cursor = con.cursor()
cursor.execute("SELECT context FROM ctx_data")
row = cursor.fetchall() #[('',),('',) ...]
raw_data = [x[0][:80] for x in row] #리스트 안의 각 튜플 형태로 저장되어 있는 원문을 :80까지만 출력
#print(row)
context = list(enumerate(raw_data,1)) #[(1,'...'),(2,'...'),(3,'...'),... ]

option = st.selectbox('Which context would you like to select?', context)
st.write('You selected:', option) #option = (#,'...')

#id, context session_state initialize
if 'id' not in st.session_state:
    st.session_state['id'] = 0
if 'context' not in st.session_state:
    st.session_state['context'] = ''
st.session_state['id'] = option[0]
st.session_state['context'] = row[option[0]-1][0] #option에서 id는 1부터 시작하기 때문에 -1
print(st.session_state['context'])


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
 
gen_button = st.button('시험지 생성')

if gen_button:
    st.session_state['gen_button_clicked'] = True

    with st.spinner('Wait for it...'):
        for i in range(q_number):
            if 'q' not in st.session_state:
                st.session_state['q'] = q_engines[q_type](st.session_state['context'],q_number) #객체 생성
#             if st.session_state['gen_button_clicked']:
#                 question = st.session_state['q'].show_q()
#                 st.session_state['q'].q_data() #질문 저장
#                 st.write(question)
            del st.session_state['q']
# st.divider()

    
