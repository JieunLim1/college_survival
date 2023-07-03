from qa import QA
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
class FRQ(QA):
    def __init__(self,context):
        super().__init__(context)

    def make_q(self):
        messages = [
            SystemMessage(content="""Create a free-response question in the text and outputting a JSON object with an array of these entities, using the following format:
            input:
            "Social facilitation is an individual's improved performance on easy or well-learned tasks when they are with others. When others observe us, we become aroused, which solicits the most likely response to a stimulus. This means that we will perform better on easy tasks, but worse on difficult tasks. The tendency to perform worse on difficult tasks is called social inhibition. 
            output:
            {"Question": "What is social facilitation? How does it affect an individual's performance on tasks?", 
            "Model Answer" : "Social facilitation is a phenomenon where an individual performs better on easy or well-learned tasks when they are in the presence of others."}
            """
            ),
            HumanMessage(content = self.context)
        ]   
        result = self.chat(messages)
        result = result.content
        jdata = json.loads(result,strict = False)
        return jdata
    
    def show_q(self):
            return self.q['Question']

    def scoring(self, answer : str):
        self.answer = answer
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
            HumanMessage(content = ("Model Answer : " + self.q['Model Answer'] + ", User response : " + self.answer))
            ]
        result = self.chat(messages)
        self.result = result.content
        self.jdata = json.loads(result,strict = False)
        if float(self.jdata['Similarity']) < 0.8:
            self.result = "Your estimated score: " + self.jdata['Similarity'] + "\n" + "Incorrect. " + self.jdata['Things to improve'] + " You could look upon " + self.jdata['Key Term(s)']
            return self.result
        else:
            self.result = "Your estimated score: " + self.jdata['Similarity'] + "\n" + "Correct. "+ "If you would like to improve more, please refer below: " + self.jdata['Things to improve']
            return self.result

        
    def record(self, date : str):
        con = sq3.connect("record1.db", isolation_level=None)
        cursor = con.cursor()
        cursor.execute('CREATE TABLE if not exists questions_data(date TEXT, context TEXT, question TEXT, input TEXT, result TEXT)')

        data_list = (date,self.context,self.q['Question'],self.answer,self.result)
        cursor.execute('Insert INTO questions_data(date, context, question, input, result) \
                    VALUES(?,?,?,?,?)', data_list)
        cursor.close()
