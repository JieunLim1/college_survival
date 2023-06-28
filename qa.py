from abc import ABC
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

# [TODO] QA class를 이용해서 FRQ와 MCQ를 정리하기.

class QA(ABC):
    def __init__(self, context):
        # openai 연결 부분 초기화
        self.context = context
        self.q = self.make_q()
        self.show_q()
        self.user_input = input("Enter your answer : ")
        
    
    def make_q(self):
        # 문제 정보를 생성하고, self에 저장한다.
        pass

    def show_q(self):
        #self 안에 저장된 문제 (w/ 선택사항) 프린트
        pass        

    def scoring(self, user_answer):
        # 정답 여부를 측정한다.
        # 문제의 정보는 self 안에 있다.
        pass
    
    def feedback(self):
        # self 안의 정보를 토대로 사용자에게 피드백을 반환한다.
        pass
