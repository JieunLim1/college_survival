import streamlit as st
import sqlite3 as sq3

st.set_page_config(page_title="Things I must review", page_icon="📌")
st.markdown(""" # Correction Note 
----
Review questions that you have written wrong""")
st.subheader("무슨 과목의 오답노트를 생성하시겠습니까?")
con = sq3.connect('record1.db',isolation_level = None)
cursor = con.cursor()
subject_list = cursor.execute("SELECT * FROM subject_data")
option = st.selectbox("PICK a SUBJECT",subject_list) 

if 'correction_button' not in st.session_state:
    st.session_state['correction_button'] = False
correction_button = st.button("오답노트 생성")

if correction_button:
    st.session_state['correction_button'] = True
    subject = option[1] #subject 내용
    subject_id = option[0] #subject index 
    cursor.execute("CREATE TABLE if not exists incorrect_table(question_id INTEGER ,question TEXT, subject TEXT, context TEXT, answer TEXT, score REAL)")
    cursor.execute("""INSERT INTO incorrect_table(question_id, question, subject, context, answer , score ) SELECT question.id, question.question, subject, context, question.answer, score FROM subject_data 
                        join ctx_data on subject_data.id = ctx_data.subject_id 
                        join question on ctx_data.id = question.context_id
                        join response_data on response_data.score < 0.8""")
    cursor.execute("SELECT question_id,question,answer FROM incorrect_table WHERE subject = ?",(subject,))
    incorrect_data = cursor.fetchall()
    print(incorrect_data)
    results = [] 
    count = 0
    for i in range(len(incorrect_data)):
        st.write(incorrect_data[i][1])
        response = st.text_input("여기에 답을 입력하시오.", key = count)
        results.append(response)
        st.write(incorrect_data[i][2])
        count += 1
        



    


