import streamlit as st
import sqlite3 as sq3
st.set_page_config(page_title="Saving Context", page_icon="🗂️")
st.sidebar.header("Saving Your Context")

st.title("Welcome!")
st.subheader("This page is to record your entered context and categorize it into subjects.")
st.session_state['context'] = st.text_area("여기에 저장할 원문을 적어주세요.")
st.session_state['subject'] = st.text_input("위 원문은 어떤 과목에 해당하나요?")
st.session_state['save_button_clicked'] = False
save_button = st.button('저장하기')

con = sq3.connect("record1.db", isolation_level = None)
cursor = con.cursor()

if save_button:
    st.session_state['save_button_clicked'] = True
if st.session_state['save_button_clicked']:
    #원문에 따른 과목 저장
    cursor.execute('CREATE TABLE if not exists subject_data(id INTEGER PRIMARY KEY AUTOINCREMENT)')
    cursor.execute('Insert INTO subject_data(subject) VALUES(?)', (st.session_state['subject'],))
    id = cursor.lastrowid
    print(id)
    #원문 저장
    cursor.execute("""CREATE TABLE if not exists ctx_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, context TEXT, subject_id INTEGER)""")
    cursor.execute('Insert INTO ctx_data(context) VALUES(?,?)',(st.session_state['context'],id))
    con.commit()


