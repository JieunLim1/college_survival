from abc import ABC

# [TODO] QA class를 이용해서 FRQ와 MCQ를 정리하기.

class QA(ABC):
    def __init__(self, context):
        self.context = context
        self.make_q()
        # openai 연결 부분 초기화
    
    def make_q(self):
        # 문제 정보를 생성하고, self에 저장한다.
        pass
    
    def scoring(self, user_answer):
        # 정답 여부를 측정한다.
        # 문제의 정보는 self 안에 있다.
        pass
    
    def feedback(self):
        # self 안의 정보를 토대로 사용자에게 피드백을 반환한다.
        pass


# q = FRQ('텍스트')
# q = MCQ('텍스트')
q.scoring()
print(q.feedback())