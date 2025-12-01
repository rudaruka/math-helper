import streamlit as st

st.title("🧮 수학 도우미 mini")

menu = st.selectbox("무슨 계산을 도와줄까?", ["기본 사칙연산", "일차함수 y=ax+b 풀기"])

if menu == "기본 사칙연산":
    a = st.number_input("첫 번째 수", value=1.0)
    b = st.number_input("두 번째 수", value=1.0)
    op = st.selectbox("연산", ["+", "-", "×", "÷"])

    if st.button("계산하기"):
        if op == "+": st.write(a + b)
        elif op == "-": st.write(a - b)
        elif op == "×": st.write(a * b)
        elif op == "÷":
            st.write(a / b if b != 0 else "0으로 나눌 수 없음")

elif menu == "일차함수 y=ax+b 풀기":
    a = st.number_input("a 값")
    b = st.number_input("b 값")
    x = st.number_input("x 값")
    if st.button("y 값 구하기"):
        st.write(f"y = {a*x + b}")
