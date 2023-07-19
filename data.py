import sqlite3 as sq3
import Folder.app as app

def connection():
    con = sq3.connect("record1.db")
    return con

def create_ctx(con):
    cursor = con.cursor()
    cursor.execute('CREATE TABLE questions_data(date TEXT, context TEXT, question TEXT, input TEXT, result TEXT)')
    con.commit()

def insert(con,one_data):
    cursor = con.cursor()
    cursor.execute('Insert INTO questions_data(date, context, question, input, result) VALUES(?,?,?,?)', one_data)
    con.commmit()



# con = connection()
# create(con)
# data_list = (app.st.session['time'],app.context,app.question,app.st.session_state['user_answer'],app.result)
# insert(con,data_list)

