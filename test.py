
import json

def make_question(input_str=""):
    # chatgpt가 뭔가 하게 하는 부분이 작성되어야 함
    result = """
        {
        "문제": "문제....",
        "문항": "문항....",
        "정답번호": 3,
        "해설": "해설...."
        }
        """  # 이 부분은 지워야 함
    return json.loads(result)

def scoring(user_answer: int, question: dict):
    if (user_answer == question['정답번호']):
        return True
    print(question['해설'])
    return False


if __name__ == '__main__':
    question = make_question() # 데이터를 입력 받는 부분이 작성되어야 함
    print(question['문제'])
    print(question['문항'])
    user_answer = int(input('user >> '))

    print(scoring(user_answer, question))