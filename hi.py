import streamlit as st
import pandas as pd
import sqlite3 as sq3

con = sq3.connect("record1.db", isolation_level = None)
cursor = con.cursor()
cursor.execute('SELECT * FROM questions_data')
rowList = cursor.fetchall()
cols = [column[0] for column in cursor.description]
df = pd.DataFrame.from_records(data=rowList, columns=cols)

st.sidebar.title('📈 Make Your Graph & Chart 📉')
option = st.sidebar.selectbox(
    'Based on what category would you like to make your graph?',
    ['question', 'all']
    )
st.sidebar.write('You selected:', option)

con1 = sq3.connect("record2.db", isolation_level=None)
cursor1 = con1.cursor()
cursor1.execute('CREATE TABLE if not exists sample_data(question TEXT, input TEXT, score REAL)')

if option == 'question':
     tmp_df = df['question']
else:
    tmp_df = df['score']
samplehead_df = tmp_df.head()
st.table(samplehead_df)

pick = st.radio("Based on which question would you like to make a graph?", [1,2,3,4])
#options = list(range(df.head().count()))
for i in df.index:
    if df.loc[i,'question'] == tmp_df.loc[int(pick),'question']:
        cursor1.execute('Insert INTO questions_data(question, input, score) \
                    VALUES(?,?,?,?,?,?)', df.loc[i]['question'],df.loc[i]['input'],df.loc[i]['score'])
        con1.commit()
cursor1.execute('SELECT * FROM questions_data')
rowList = cursor1.fetchall()
cols = [column[0] for column in cursor1.description]
df = pd.DataFrame.from_records(data=rowList, columns=cols)
st.line_chart(df)

#  record_button = st.button('기록보기')    
#         if record_button:
#             st.session_state['recording_button_clicked'] = True
            
#         if st.session_state['recording_button_clicked']:
#             con = sq3.connect("record1.db", isolation_level = None)
#             cursor = con.cursor()
#             cursor.execute('SELECT score FROM questions_data')
#             rowList = cursor.fetchall()
#             print(rowList)
#             df = pd.DataFrame(rowList, columns = ['score'])
#             st.subheader('This is your GRAPH')
#             st.line_chart(df)
#             con.close()
#         # chart_button = st.button('결과표 보기')
#         # if chart_button:
#         # st.session_state['chart_button_clicked'] = True
#         # if st.session_state['chart_button_clicked']:
            




