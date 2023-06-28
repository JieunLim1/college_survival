from qa import QA
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
class FRQ(QA):
    def __init__(self,context):
        super().__init__(context)
        self.data = self.scoring()
        self.feedback()

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
        result = chat(messages)
        result = result.content
        jdata = json.loads(result,strict = False)
        return jdata
    
    def show_q(self):
            print (self.q['Question'])

    def scoring(self):
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
            HumanMessage(content = ("Model Answer : " + self.q['Model Answer'] + ", User response : " + self.user_input))
        ]   
        result = chat(messages)
        result = result.content
        jdata = json.loads(result,strict = False)
        return jdata

    def feedback(self):
        print("Your estimated score: " + self.data['Similarity'])
        if float(self.data['Similarity']) < 0.8:
            print("Incorrect. " + self.data['Things to improve'] + " You could look upon " + self.data['Key Term(s)'] + ".")
        else:
            print("Correct. "+ "If you would like to improve more, please refer below: " + self.data['Things to improve'])

#q1 = FRQ("""The mere exposure effect in psychology, or the familiarity principle, is the idea that people tend to prefer things that are familiar. This means that having already encountered something creates a preference for it. For example, when people are repeatedly exposed to advertisements, they tend to favor the product because it is more familiar than brands they are not familiar with. The mere exposure effect applies to every area of a person's life, including people, things, words, paintings, and sounds.
#        """)
