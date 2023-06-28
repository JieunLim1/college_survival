import streamlit as st

# pip install streamlit
# 실행 명령어 : streamlit run app.py

# [TODO] GUI 형태로 만들어보기.
st.markdown("""# 대학생 구원자
---
- 이 앱은 학업에 지친 대학생에게 도움이 되고자 개발되어 필기한 내용들을 바탕으로 문제를 생성시켜 복습을 도와주는데 효율적입니다.
""")

context = st.text_area('여기에 문제를 생성할 원문을 적어주세요.')
#파일 받는 것도 만들어보기

q_type = st.radio(
    "문제의 유형을 선택해주세요",
    ('FRQ', 'MCQ'))

st.divider() # 구분 짓는 선 긋기

from FRQ import FRQ
from MCQ import MCQ

q_engines = {
    'FRQ': FRQ,
    'MCQ': MCQ
    }

if st.button('문제 생성'):
    st.write(q_type)
    q1 = q_engines[q_type](context) #객체 생성
    question = q1.show_q()
    st.write(question) # 질문 띄우기
    user_answer = st.text_input("Enter your answer : ") #사용자로부터 입력값 받기

    if st.button('Confirm'):
        result = q1.scoring(user_answer) # 채점
        st.write(result) #채점한 결과 띄우기
