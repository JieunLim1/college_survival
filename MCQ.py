import os
import json
from qa import QA
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


class MCQ(QA):

    def __init__(self,context):
        super().__init__(context)

    def make_q(self):
        messages = [
            SystemMessage(content="""Create a multiple-choice question in the text and outputting a JSON object with an array of these entities, using the following format:
            input:
            "The applications of language models include:
            • Auto-completion
            • Document summarization: Generating the most likely words for a summary after understanding the content of a document
            • Machine translation: Converting the English language to the Korean language by using a language understanding model in conjunction with a numerical output value, which is then translated back to the English language.
            • Dialogue systems: Evaluating the most probable words required during a conversation and generating sentences accordingly"
            output:
            {"Question": "What are the possible applications of language models?","Options" :{"A":"Auto-completion","B": "Document summarization","C": "Machine translation","D": "All of the above"},"Answer": "D","Explanation" : "Language models can be applied in various tasks such as auto-completion, document summarization, machine translation, speech recognition, dialogue systems, and even sentence creation."}"""
            ),
            HumanMessage(content=self.context)
        ]   
        result = self.chat(messages)
        result = result.content 
        jdata = json.loads(result,strict = False) #\n과 같은 제어 문자 허용
        return jdata
    
    def show_q(self):
            return self.q['Question'], self.q['Options']

    def scoring(self, answer : str):
        if answer == self.q["Answer"]:
            return "Correct, " + self.q['Explanation']
        else:
            return "Incorrect, " + self.q["Explanation"]
