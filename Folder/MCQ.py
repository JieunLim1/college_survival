import os
import json
from qa import QA
from dotenv import load_dotenv
import sqlite3 as sq3
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


class MCQ(QA):

    def __init__(self,context,num,ctx_id):
        super().__init__(context,num,ctx_id)

    def make_q(self):
        messages = []
        self.qid_list = []
        self.results = []
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists question(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, question TEXT, context_id INTEGER)')
        prompt1 = """Create a multiple-choice question in the text and outputting a JSON object with an array of these entities, using the following format:
            input:
            "The applications of language models include:
            • Auto-completion
            • Document summarization: Generating the most likely words for a summary after understanding the content of a document
            • Machine translation: Converting the English language to the Korean language by using a language understanding model in conjunction with a numerical output value, which is then translated back to the English language.
            • Dialogue systems: Evaluating the most probable words required during a conversation and generating sentences accordingly"
            output:
            {"Question": "What are the possible applications of language models?","Options" :{"A":"Auto-completion","B": "Document summarization","C": "Machine translation","D": "All of the above"},"Answer": "D","Explanation" : "Language models can be applied in various tasks such as auto-completion, document summarization, machine translation, speech recognition, dialogue systems, and even sentence creation."}"""
        message = [SystemMessage(content=prompt1),
                    HumanMessage(content=self.context)]
        result = self.chat(message)
        result = result.content
        result = json.loads(result,strict = False)
        messages.append(message)
        self.results.append(result) #\n과 같은 제어 문자 허용 
        cursor.execute('Insert INTO question(question,context_id,answer) VALUES(?,?,?)', [result['Question'],self.ctx_id,result['Answer']])
        self.qid_list.append(cursor.lastrowid)

        prompt2 = """Create another question that is different from previosuly created questions. But keep the output format the same.       
            output:
            {"Question": "What are the possible applications of language models?","Options" :{"A":"Auto-completion","B": "Document summarization","C": "Machine translation","D": "All of the above"},"Answer": "D","Explanation" : "Language models can be applied in various tasks such as auto-completion, document summarization, machine translation, speech recognition, dialogue systems, and even sentence creation."}"""
        for i in range(self.num-1):
            message = [SystemMessage(content = prompt2),HumanMessage(content = self.context)]
            result = self.chat(message)
            result = result.content
            result = json.loads(result,strict = False)
            messages.append(message)
            self.results.append(result)
            qo = result['Question'] + " " + str(result['Options'])
            cursor.execute('Insert INTO question(question,context_id) VALUES(?,?)', [qo,self.ctx_id])
            self.qid_list.append(cursor.lastrowid)
        print(self.results)
        return self.results
    
    def show_q(self):
        self.q_list = []
        self.answer_list = []
        self.explanation_list = []
        for i in range(len(self.q)):
            q = self.results[i].get('Question')
            o = str(self.results[i].get('Options'))
            qo = str(i+1) + ". " + q + " Options: " + o 
            print(qo)
            self.q_list.append(qo)
            self.answer_list.append(self.results[i].get('Answer'))
            self.explanation_list.append(self.results[i].get('Explanation'))
        print(self.q_list)
        return self.q_list


    def scoring(self, response_list : list):
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists response_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, input TEXT, result TEXT, score REAL, question_id INTEGER)')
        result_list = []
        for i in range(len(response_list)):
            if response_list[i] == self.answer_list[i]:
                score = "1"
                self.result = "Correct, " + self.explanation_list[i] + " Score: " + score 
            else:
                score = "0"
                self.result = "Incorrect, " + self.explanation_list[i] + " Score: " + score 
            result_list.append(self.result)
            cursor.execute('INSERT INTO response_data(input,result,score,question_id) VALUES(?,?,?,?)',(response_list[i],self.result,score,self.qid_list[i]))
        return result_list
    
    def record(self,date):
        self.date = date
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists response_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date TEXT, input TEXT, result TEXT, score TEXT)')

        data_list = (self.date,self.input,self.result,self.q['score'])
        cursor.execute('Insert INTO response_data(date, input, result, score) VALUES(?,?,?,?)', data_list)
        con.commit()
        con.close()



