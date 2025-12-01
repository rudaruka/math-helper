import streamlit as st
import sympy as sp

st.set_page_config(page_title="수학 도우미", layout="centered")
st.title("🧮 수학 도우미")

menu = st.selectbox(
    "기능을 선택하세요",
    ["사칙연산 계산기", "일차함수 y=ax+b 계산", "방정식 풀기", "그래프 그리기"]
)

# -------------------------------------------------------
# 1) 사칙연산
# -------------------------------------------------------
if menu == "사칙연산 계산기":
    a = st.number_input("첫 번째 수", value=1.0)
    b = st.number_input("두 번째 수", value=1.0)
    op = st.selectbox("연산자", ["+", "-", "×", "÷"])

    if st.button("계산하기"):
        if op == "+": st.success(a + b)
        elif op == "-": st.success(a - b)
        elif op == "×": st.success(a * b)
        elif op == "÷":
            st.success(a / b if b != 0 else "0으로 나눌 수 없음")

# -------------------------------------------------------
# 2) 일차함수
# -------------------------------------------------------
elif menu == "일차함수 y=ax+b 계산":
    a = st.number_input("a 값", value=1.0)
    b = st.number_input("b 값", value=0.0)
    x = st.number_input("x 값", value=0.0)

    if st.button("y 값 계산"):
        st.success(a * x + b)

# -------------------------------------------------------
# 3) 방정식 풀기
# -------------------------------------------------------
elif menu == "방정식 풀기":
    eq_text = st.text_input("방정식을 입력하세요 (예: 2*x + 3 = 7)")

    if st.button("풀기"):
        try:
            x = sp.Symbol('x')
            equation = sp.Eq(*sp.sympify(eq_text).args)
            solution = sp.solve(equation, x)
            st.success(f"해: {solution}")
        except:
            st.error("방정식 형식이 잘못되었습니다.")

# -------------------------------------------------------
# 4) 그래프 그리기
# -------------------------------------------------------
elif menu == "그래프 그리기":
    function_text = st.text_input("함수를 입력하세요 (예: x**2 - 3*x + 2)")
    x = sp.Symbol('x')

    if st.button("그래프 그리기"):
        try:
            func = sp.sympify(function_text)
            plot = sp.plot(func, (x, -10, 10), show=False)
            plot.save("graph.png")
            st.image("graph.png")
        except:
            st.error("함수 형식이 잘못되었습니다.")
