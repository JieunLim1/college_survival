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
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)

class MCQ(QA):

    def __init__(self,context):
        super().__init__(context)
        #self.scoring()

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
        result = chat(messages)
        result = result.content 
        jdata = json.loads(result,strict = False) #\n과 같은 제어 문자 허용
        return jdata
    
    def show_q(self):
            print (self.q['Question'], self.q['Options'])

    def scoring(self):
        if self.user_input == self.q["Answer"]:
            print("Correct, ",self.q['Explanation'])
        else:
            print("Incorrect, ", self.q["Explanation"])

#q = MCQ("""The mere exposure effect in psychology, or the familiarity principle, is the idea that people tend to prefer things that are familiar. This means that having already encountered something creates a preference for it. For example, when people are repeatedly exposed to advertisements, they tend to favor the product because it is more familiar than brands they are not familiar with. The mere exposure effect applies to every area of a person's life, including people, things, words, paintings, and sounds.
#        """)
