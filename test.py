from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os
import json
os.environ["OPENAI_API_KEY"] = "..."

llm = OpenAI(temperature=0.9)

def make_question(input_text=""):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""{text} 를 기반으로 JSON 형식으로 Question, Options, Answer, Explanation 의 키를 가진 객관식 문제를 생성해라. option과 answer은 알파벳으로 기호를 넣는다."""
        )
    chain = LLMChain(llm=llm, prompt=prompt)
    result = json.loads(chain.run(input_text))
    return (result)

def scoring(user_answer: str, question: dict):
    if (user_answer == question['Answer']):
        print ("Correct")
        return (question['Explanation'])
    else :
        print("Incorrect")
    return (question['Answer'] , question['Explanation'])
    

if __name__ == '__main__':
    question = make_question("") # 데이터를 입력 받는 부분이 작성되어야 함
    print(question['Question'])
    print(question['Options'])
    user_answer = input('Enter your answer in a captialized alphabet >> ')

    print(scoring(user_answer, question))

