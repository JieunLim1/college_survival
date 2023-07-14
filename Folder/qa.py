from abc import ABC
import os
import json
from dotenv import load_dotenv
import sqlite3 as sq3
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# [TODO] QA class를 이용해서 FRQ와 MCQ를 정리하기.

class QA(ABC):
    input=''
    result=''
    jdata = ''

    def __init__(self, context):
        # openai 연결 부분 초기화?
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
        self.chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)
        self.context = context
        self.q = self.make_q()
        
    
    def make_q(self):
        # 문제 정보를 생성하고, self에 저장한다.
        pass

    def show_q(self):
        #self 안에 저장된 문제 (w/ 선택사항) 프린트
        pass        

    def scoring(self):
        # 정답 여부를 측정한다.
        # 문제의 정보는 self 안에 있다.
        pass
    
    def record(self): 
        #문제와 원문 그 외의 것 저장
        pass

    def q_data(self):                    #문제만 저장
        con = sq3.connect("record1.db")
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists question(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, question TEXT)')
        print(self.q)
        print(json.dumps(self.q))
        cursor.execute('INSERT INTO question(question) VALUES (?)', [json.dumps(self.q)])
        con.commit()
    
 