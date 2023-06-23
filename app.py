import streamlit as st

# [TODO] GUI 형태로 만들어보기.

st.markdown("""# 대학생 구원자
---
- 이 앱은 ~~~
""")

context = st.text_area('여기에 문제를 생성할 원문을 적어주세요.')

q_type = st.radio(
    "문제의 유형을 선택해주세요",
    ('FRQ', 'MCQ'))

# from FRQ import FreeResponseQuestion
# from MCQ import MultiChoiceQuestion

# q_engines = {
#     'FRQ': FreeResponseQuestion,
#     'MCQ': MultiChoiceQuestion
# }

if st.button('문제 생성'):
    st.write(q_type)
    # qa = q_engines[q_type](context)