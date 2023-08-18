from qa import QA
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import sqlite3 as sq3
import time

from langchain.schema import (
    HumanMessage,
    SystemMessage
)
class FRQ(QA):
    def __init__(self,context,num,ctx_id):
        super().__init__(context,num,ctx_id)
    def __init__(self,context,num,ctx_id):
        super().__init__(context,num,ctx_id)

    def make_q(self):
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists question(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, question TEXT)')
        cursor.execute('CREATE TABLE if not exists exam_ppr(id INTEGER PRIMARY KEY AUTOINCREMENT, exam TEXT)')

        messages = []
        results = []
        self.qid_list = []
        prompt = """Create a free-response question and output a JSON object with an array of these entities, using the following format:
            input:
            "Social facilitation is an individual's improved performance on easy or well-learned tasks when they are with others. When others observe us, we become aroused, which solicits the most likely response to a stimulus. This means that we will perform better on easy tasks, but worse on difficult tasks. The tendency to perform worse on difficult tasks is called social inhibition. 
            output:
            {"Question": "What is social facilitation? How does it affect an individual's performance on tasks?", 
            "Model Answer" : "Social facilitation is a phenomenon where an individual performs better on easy or well-learned tasks when they are in the presence of others."}
            """
        message = [
            SystemMessage(content= prompt),
            HumanMessage(content = self.context)] 
        for i in range(self.num):
            result = self.chat(message)
            result = result.content
            result = json.loads(result,strict = False)
            messages.append(message)
            results.append(result)
            cursor.execute('Insert INTO question(question,context_id,answer) VALUES(?,?,?)', [result['Question'],self.ctx_id,result['Model Answer']])
            self.qid_list.append(cursor.lastrowid)
            con.commit()
        return results
    
    def show_q(self):
        self.qlist = [ i['Question'] for i in self.q ]
        return self.qlist

    def scoring(self, response_list : list):
        result_list = []
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists response_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, input TEXT, result TEXT, score REAL, question_id INTEGER)')
        self.alist = [i['Model Answer'] for i in self.q]
        for i in range(len(response_list)):
            messages = [
                SystemMessage(content="""
                model answer과 user's response이 얼마나 유사한지 아래의 output 형식과 같이 나타내시오. 
                output:
                {
                "Similarity" : "0.47" , 
                "Things to improve": "The user could improve their response by using more precise terminology and providing specific examples", 
                "Key Term(s)" : "social facilitation"
                }
                """
                ),
                HumanMessage(content=("Model Answer : "+self.alist[i]+", User response : "+response_list[i]))
                ]
            result = self.chat(messages)
            result = result.content
            self.jdata = json.loads(result,strict = False)
            print("this is line 80 ",end = " " )
            print(self.jdata)
            if float(self.jdata['Similarity']) < 0.8:
                self.result = "Your estimated score: " + self.jdata['Similarity'] + "\n" + "Incorrect. " + self.jdata['Things to improve'] + " You could look upon " + self.jdata['Key Term(s)']
            else:
                self.result = "Your estimated score: " + self.jdata['Similarity'] + "\n" + "Correct. "+ "If you would like to improve more, please refer below: " + self.jdata['Things to improve']
            result_list.append(self.result)
        print(result_list)
        return result_list
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists response_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, input TEXT, result TEXT, score REAL, question_id INTEGER)')
        self.alist = [i['Model Answer'] for i in self.q]
        for i in range(len(response_list)):
            messages = [
                SystemMessage(content="""
                model answer과 user's response이 얼마나 유사한지 아래의 output 형식과 같이 나타내시오. 
                output:
                {
                "Similarity" : "0.47" , 
                "Things to improve": "The user could improve their response by using more precise terminology and providing specific examples", 
                "Key Term(s)" : "social facilitation"
                }
                """
                ),
                HumanMessage(content=("Model Answer : "+self.alist[i]+", User response : "+response_list[i]))
                ]
            result = self.chat(messages)
            result = result.content
            self.jdata = json.loads(result,strict = False)
            print("this is line 80 ",end = " " )
            print(self.jdata)
            if float(self.jdata['Similarity']) < 0.8:
                self.result = "Your estimated score: " + self.jdata['Similarity'] + "\n" + "Incorrect. " + self.jdata['Things to improve'] + " You could look upon " + self.jdata['Key Term(s)']
            else:
                self.result = "Your estimated score: " + self.jdata['Similarity'] + "\n" + "Correct. "+ "If you would like to improve more, please refer below: " + self.jdata['Things to improve']
            result_list.append(self.result)
        print(result_list)
        return result_list
        
    # def record(self,date):
    #     self.date = date
    #     con = sq3.connect("record1.db", isolation_level=None)
    #     cursor = con.cursor()
    #     cursor.execute('CREATE TABLE if not exists response_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date TEXT, input TEXT, result TEXT, score REAL)')

        data_list = (self.date,self.input,self.result,float(self.jdata['Similarity']))
        cursor.execute('Insert INTO response_data(date, input, result, score) \
                    VALUES(?,?,?,?)', data_list)
        con.commit()
        con.close()

    
            
