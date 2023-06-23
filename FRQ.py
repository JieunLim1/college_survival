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

def make_q(user_input=""):
    messages = [
        SystemMessage(content="""Create a free-response question in the text and outputting a JSON object with an array of these entities, using the following format:
        input:
        "Social facilitation is an individual's improved performance on easy or well-learned tasks when they are with others. When others observe us, we become aroused, which solicits the most likely response to a stimulus. This means that we will perform better on easy tasks, but worse on difficult tasks. The tendency to perform worse on difficult tasks is called social inhibition. 
        output:
        {"Question": "What is social facilitation? How does it affect an individual's performance on tasks?", 
        "Model Answer" : "Social facilitation is a phenomenon where an individual performs better on easy or well-learned tasks when they are in the presence of others."}
        """
        ),
        HumanMessage(content = user_input)
    ]   
    result = chat(messages)
    result = result.content
    jdata = json.loads(result,strict = False)
    return jdata

def scoring(user_input: str):
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
        HumanMessage(content = user_input)
    ]   
    result = chat(messages)
    result = result.content
    jdata = json.loads(result,strict = False)
    return jdata

def printing(q : dict):
    print("Your estimated score: " + q['Similarity'])
    if float(q['Similarity']) < 0.8:
        print("Incorrect. " + q['Things to improve'] + " You could look upon " + q['Key Term(s)' + "."])
    else:
        print("Correct. "+ "If you would like to improve more, please refer below: " + q['Things to improve'])

if __name__ == '__main__':
    text = input("Enter the text: ")
    question = make_q(text) 
    print("Question : " + question["Question"])
    answer = question['Model Answer'] 
    user_input = input("Enter your answer : ")
    combined_str = "Model Answer : " + answer + ", User response : " + user_input
    question2 = scoring(combined_str)
    printing(question2)
    

