import streamlit as st
import sympy as sp
import math

st.set_page_config(page_title="중등 수학 도우미", layout="wide")
st.title("📘 중학생 수학 도우미 — 계산/그래프/공식 한곳에")

menu = st.sidebar.selectbox(
    "학년을 선택하세요",
    ["중1", "중2", "중3"]
)

# ======================================================
# 공통: 입력 보조
# ======================================================
def float_input(label, value=0.0):
    return st.number_input(label, value=float(value))

x = sp.Symbol('x')

# ======================================================
# 🟦 중1 기능
# ======================================================
if menu == "중1":
    topic = st.selectbox(
        "단원을 선택하세요",
        [
            "사칙연산",
            "정수와 유리수",
            "소인수분해",
            "최대공약수·최소공배수",
            "일차방정식",
            "좌표평면",
            "도형 — 삼각형·사각형 넓이"
        ]
    )

    # 사칙연산
    if topic == "사칙연산":
        a = float_input("첫 번째 수", 1)
        b = float_input("두 번째 수", 1)
        op = st.selectbox("연산자", ["+", "-", "×", "÷"])
        if st.button("계산"):
            if op == "+": st.success(a+b)
            elif op == "-": st.success(a-b)
            elif op == "×": st.success(a*b)
            elif op == "÷": st.success(a/b if b!=0 else "0으로 나눌 수 없음")

    # 정수/유리수 관련
    elif topic == "정수와 유리수":
        st.write("정수/유리수 정리: 분수 → 소수 변환")
        num = float_input("분자")
        den = float_input("분모")
        if st.button("변환"):
            if den == 0: st.error("0으로 나눌 수 없음")
            else:
                st.write("소수 =", num/den)

    # 소인수분해
    elif topic == "소인수분해":
        n = st.number_input("수를 입력(양의 정수)", value=12, step=1)
        if st.button("분해"):
            st.success(sp.factorint(int(n)))

    # 최대공약수/최소공배수
    elif topic == "최대공약수·최소공배수":
        a = st.number_input("a", value=12, step=1)
        b = st.number_input("b", value=18, step=1)
        if st.button("계산"):
            st.write("GCD =", math.gcd(int(a), int(b)))
            st.write("LCM =", abs(a*b)//math.gcd(int(a), int(b)))

    # 일차방정식 (ax + b = c)
    elif topic == "일차방정식":
        eq_text = st.text_input("예: 2*x + 3 = 11")
        if st.button("풀기"):
            try:
                eq = sp.Eq(*sp.sympify(eq_text).args)
                st.success(sp.solve(eq, x))
            except:
                st.error("형식을 다시 확인하세요.")

    # 좌표평면 점 사이 거리
    elif topic == "좌표평면":
        x1 = float_input("x1")
        y1 = float_input("y1")
        x2 = float_input("x2")
        y2 = float_input("y2")
        if st.button("거리 계산"):
            st.success(math.sqrt((x1-x2)**2 + (y1-y2)**2))

    # 도형 넓이
    elif topic == "도형 — 삼각형·사각형 넓이":
        shape = st.selectbox("도형", ["삼각형", "직사각형", "평행사변형"])
        if shape == "삼각형":
            b = float_input("밑변")
            h = float_input("높이")
            if st.button("넓이"):
                st.success(b*h/2)
        elif shape == "직사각형":
            w = float_input("가로")
            h = float_input("세로")
            if st.button("넓이"):
                st.success(w*h)
        else:  # 평행사변형
            b = float_input("밑변")
            h = float_input("높이")
            if st.button("넓이"):
                st.success(b*h)

# ======================================================
# 🟩 중2 기능
# ======================================================
elif menu == "중2":
    topic = st.selectbox(
        "단원 선택",
        [
            "식의 계산",
            "연립방정식",
            "일차함수 y=ax+b",
            "일차함수 그래프",
            "유리수·순환소수",
            "도형 — 원 넓이/호의 길이"
        ]
    )

    # 식의 계산 (인수분해/전개)
    if topic == "식의 계산":
        expr = st.text_input("식을 입력 (예: (x+3)*(x-2))")
        mode = st.selectbox("기능", ["전개", "인수분해"])
        if st.button("실행"):
            try:
                e = sp.sympify(expr)
                if mode == "전개":
                    st.success(sp.expand(e))
                else:
                    st.success(sp.factor(e))
            except:
                st.error("식을 확인하세요.")

    # 연립방정식
    elif topic == "연립방정식":
        st.write("예: 2*x + y = 7  /  x - y = 1")
        eq1 = st.text_input("1번 식")
        eq2 = st.text_input("2번 식")
        if st.button("풀기"):
            try:
                X, Y = sp.symbols('x y')
                sol = sp.solve([eq1, eq2], [X, Y])
                st.success(sol)
            except:
                st.error("형식을 확인하세요.")

    # 일차함수 계산
    elif topic == "일차함수 y=ax+b":
        a = float_input("a")
        b = float_input("b")
        xv = float_input("x 값")
        if st.button("y 계산"):
            st.success(a*xv + b)

    # 일차함수 그래프
    elif topic == "일차함수 그래프":
        func = st.text_input("함수식 (예: 2*x + 3)")
        if st.button("그래프 그리기"):
            try:
                f = sp.sympify(func)
                p = sp.plot(f, (x, -10, 10), show=False)
                p.save("g.png")
                st.image("g.png")
            except:
                st.error("식을 확인!")

    # 순환소수 변환
    elif topic == "유리수·순환소수":
        num = float_input("분자", 1)
        den = float_input("분모", 3)
        if st.button("변환"):
            st.write("소수:", num/den)

    # 원 넓이 / 호의 길이
    elif topic == "도형 — 원 넓이/호의 길이":
        r = float_input("반지름")
        ang = float_input("중심각 (도)")
        if st.button("계산"):
            st.write("원 넓이 =", math.pi*r*r)
            st.write("호의 길이 =", 2*math.pi*r*(ang/360))

# ======================================================
# 🟥 중3 기능
# ======================================================
elif menu == "중3":
    topic = st.selectbox(
        "단원 선택",
        [
            "이차방정식",
            "이차함수 y=ax^2+bx+c",
            "이차함수 그래프",
            "피타고라스 정리",
            "삼각비",
            "확률"
        ]
    )

    # 이차방정식
    if topic == "이차방정식":
        eq = st.text_input("예: x**2 - 5*x + 6 = 0")
        if st.button("해 구하기"):
            try:
                e = sp.Eq(*sp.sympify(eq).args)
                st.success(sp.solve(e, x))
            except:
                st.error("식을 다시 확인.")

    # 이차함수 계산
    elif topic == "이차함수 y=ax^2+bx+c":
        a = float_input("a")
        b = float_input("b")
        c = float_input("c")
        xv = float_input("x 값")
        if st.button("y 계산"):
            st.success(a*xv*xv + b*xv + c)

    # 그래프
    elif topic == "이차함수 그래프":
        func = st.text_input("예: x**2 - 4*x + 3")
        if st.button("그리기"):
            try:
                f = sp.sympify(func)
                p = sp.plot(f, (x, -10, 10), show=False)
                p.save("quad.png")
                st.image("quad.png")
            except:
                st.error("식을 다시 확인.")

    # 피타고라스
    elif topic == "피타고라스 정리":
        a = float_input("a 변")
        b = float_input("b 변")
        if st.button("빗변"):
            st.success(math.sqrt(a*a + b*b))

    # 삼각비
    elif topic == "삼각비":
        ang = float_input("각도(도 단위)")
        if st.button("계산"):
            r = math.radians(ang)
            st.write("sin =", math.sin(r))
            st.write("cos =", math.cos(r))
            st.write("tan =", math.tan(r))

    # 확률
    elif topic == "확률":
        good = st.number_input("좋은 경우의 수", value=1, step=1)
        total = st.number_input("전체 경우의 수", value=6, step=1)
        if st.button("확률 계산"):
            st.success(good/total if total!=0 else "전체 경우=0 불가")
