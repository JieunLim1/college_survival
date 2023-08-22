import streamlit as st
import sqlite3 as sq3
import pandas as pd
  
st.set_page_config(
    page_title="Generating Your Exam Paper",
    page_icon="📝",
)
st.sidebar.success("Select a demo above.")
  
st.markdown(""" # Your Test Paper 
----
Create Your Test Paper""")

con = sq3.connect("record1.db", isolation_level = None)
cursor = con.cursor()
cursor.execute("SELECT context FROM ctx_data")
row = cursor.fetchall() #[('',),('',) ...]
raw_data = [x[0][:80] for x in row] #리스트 안의 각 튜플 형태로 저장되어 있는 원문을 :80까지만 출력
#print(row)
context = list(enumerate(raw_data,1)) #[(1,'...'),(2,'...'),(3,'...'),... ]

option = st.selectbox('Which context would you like to select?', context)
st.write('You selected:', option) #option = (#,'...')                   
q_number = st.text_input("몇개의 질문을 생성하시겠습니까?")
if q_number != None and q_number != '':
    q_number = int(q_number)




#id, context session_state initialize
if 'id' not in st.session_state:
    st.session_state['id'] = 0
if 'context' not in st.session_state:
    st.session_state['context'] = ''
st.session_state['id'] = option[0]
st.session_state['context'] = row[option[0]-1][0] #option에서 id는 1부터 시작하기 때문에 -1

#context 분할

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
    if 'q' not in st.session_state:
        st.session_state['q'] = q_engines[q_type](st.session_state['context'],q_number,st.session_state['id']) #객체 생성
        #cursor.execute('CREATE TABLE if not exists exam_ppr(id INTEGER PRIMARY KEY AUTOINCREMENT, exam TEXT)')

    qlist = st.session_state['q'].show_q() # 질문 띄우기
    #cursor.execute('INSERT INTO exam_ppr(id,exam_paper) VALUES(?)', (q_text))
    #cursor.execute('INSERT INTO examppr_question(question_id, examppr_id) VALUES (?,?)', (,examppr_id))
    #cursor.execute()

if st.session_state['gen_button_clicked']:
    response_list = []
    results = []
    count = 0
    for i in range(len(qlist)):
        if 'response' not in st.session_state:
            st.session_state['response'] = None
        q_text = qlist[i]
        st.write(q_text)
        st.session_state['response'] = st.text_input("Type Your Answer", key = count)
        response_list.append(st.session_state['response'])
        count += 1
    if '채점하기' not in st.session_state:
        st.session_state["채점하기"] = False
    btn_clicked = st.button("채점하기")
    if btn_clicked:
        st.session_state["채점하기"] = True
        if st.session_state["채점하기"]:
            results = st.session_state['q'].scoring(response_list)
        for i in range(len(st.session_state['q'].scoring(response_list))):
            st.write(str(i+1) + " " + st.session_state['q'].scoring(response_list)[i])
con.close()





        

    
