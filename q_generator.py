import os
import json
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

def make_q(user_input=""):
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
        HumanMessage(content=user_input)
    ]   
    result = chat(messages)
    result = result.content
    jdata = json.loads(result,strict = False)
    return jdata
    
def scoring(user_answer: str, q : dict):
    if user_answer == q["Answer"]:
        print("Correct, ", q['Explanation'])
    else:
        print("Incorrect, ", q["Explanation"])
    
if __name__ == '__main__':
    text = input("Enter the text: ")
    question = make_q(text) 
    print(question["Question"],question["Options"])
    user_input = input("Enter your answer : ")
    scoring(user_input,question)

