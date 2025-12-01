import streamlit as st
import sympy as sp
import math

# ==========================================
# ✨ Custom Pastel Theme (Sky Blue + Soft Pink)
# ==========================================
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #dff3ff 0%, #ffe6f2 100%);
        }
        .stApp {
            background: transparent;
        }
        .main-title {
            text-align: center;
            padding: 12px;
            font-size: 40px;
            font-weight: 700;
            color: #5a6ea8;
            border-radius: 20px;
            background: rgba(255,255,255,0.5);
            backdrop-filter: blur(8px);
        }
        .section-box {
            padding: 20px;
            background: rgba(255,255,255,0.6);
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🌈 중학생 올인원 수학 도우미</div>', unsafe_allow_html=True)
st.write(" ")

menu = st.sidebar.selectbox("학년 선택", ["중1", "중2", " 중3", "추가 단원"])
x = sp.Symbol('x')

def float_input(label, value=0.0):
    return st.number_input(label, value=float(value))

# ---------------- 중1 ----------------
if menu == "중1":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    topic = st.selectbox("중1 단원 선택", [
        "사칙연산", "정수/유리수 변환", "소인수분해",
        "최대공약수·최소공배수", "일차방정식", "좌표평면 거리",
        "도형 넓이", "원 넓이"
    ])

    if topic == "사칙연산":
        a = float_input("첫 번째 수", 1)
        b = float_input("두 번째 수", 1)
        op = st.selectbox("연산자", ["+", "-", "×", "÷"])
        if st.button("계산"):
            if op == "+": st.success(a+b)
            elif op == "-": st.success(a-b)
            elif op == "×": st.success(a*b)
            elif op == "÷": st.success(a/b if b!=0 else "0으로 나눌 수 없음")

    elif topic == "정수/유리수 변환":
        num = float_input("분자")
        den = float_input("분모")
        if st.button("변환"):
            st.success(num/den if den!=0 else "0으로 나누기 불가")

    elif topic == "소인수분해":
        n = st.number_input("양의 정수 입력", value=12, step=1)
        if st.button("분해"):
            st.success(sp.factorint(int(n)))

    elif topic == "최대공약수·최소공배수":
        a = st.number_input("a", value=12, step=1)
        b = st.number_input("b", value=18, step=1)
        if st.button("계산"):
            g = math.gcd(int(a), int(b))
            l = abs(a*b)//g
            st.write("GCD =", g)
            st.write("LCM =", l)

    elif topic == "일차방정식":
        eq_text = st.text_input("예: 2*x + 3 = 11")
        if st.button("풀이"):
            try:
                eq = sp.Eq(*sp.sympify(eq_text).args)
                st.success(sp.solve(eq, x))
            except:
                st.error("식 오류")

    elif topic == "좌표평면 거리":
        x1 = float_input("x1")
        y1 = float_input("y1")
        x2 = float_input("x2")
        y2 = float_input("y2")
        if st.button("거리 계산"):
            st.success(math.dist([x1,y1],[x2,y2]))

    elif topic == "도형 넓이":
        shape = st.selectbox("도형", ["삼각형", "직사각형", "평행사변형"])
        if st.button("넓이"):
            if shape == "삼각형":
                st.success(float_input("밑변") * float_input("높이") / 2)
            elif shape == "직사각형":
                st.success(float_input("가로") * float_input("세로"))
            else:
                st.success(float_input("밑변") * float_input("높이"))

    elif topic == "원 넓이":
        r = float_input("반지름")
        if st.button("계산"):
            st.success(math.pi*r*r)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 중2 ----------------
elif menu == "중2":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    topic = st.selectbox("중2 단원 선택", [
        "식의 전개/인수분해", "연립방정식", "일차함수 값", "일차함수 그래프",
        "유리수·순환소수", "원둘레·호의 길이", "도형 — 피타고라스 확장"
    ])

    if topic == "식의 전개/인수분해":
        expr = st.text_input("식 입력")
        mode = st.selectbox("모드", ["전개", "인수분해"])
        if st.button("실행"):
            try:
                e = sp.sympify(expr)
                st.success(sp.expand(e) if mode=="전개" else sp.factor(e))
            except:
                st.error("식 오류")

    elif topic == "연립방정식":
        eq1 = st.text_input("식 1")
        eq2 = st.text_input("식 2")
        if st.button("풀이"):
            try:
                X,Y = sp.symbols('x y')
                st.success(sp.solve([eq1, eq2], [X,Y]))
            except:
                st.error("입력 오류")

    elif topic == "일차함수 그래프":
        func = st.text_input("예: 2*x + 3")
        if st.button("그래프"):
            try:
                f = sp.sympify(func)
                p = sp.plot(f, (x,-10,10), show=False)
                p.save("l.png")
                st.image("l.png")
            except:
                st.error("식 오류")

    elif topic == "일차함수 값":
        a = float_input("a")
        b = float_input("b")
        xv = float_input("x 값")
        if st.button("계산"):
            st.success(a*xv + b)

    elif topic == "유리수·순환소수":
        num = float_input("분자",1)
        den = float_input("분모",3)
        if st.button("변환"):
            st.success(num/den)

    elif topic == "원둘레·호의 길이":
        r = float_input("반지름")
        ang = float_input("중심각(도)")
        if st.button("계산"):
            st.write("원둘레 =", 2*math.pi*r)
            st.write("호의 길이 =", 2*math.pi*r*(ang/360))

    elif topic == "도형 — 피타고라스 확장":
        a = float_input("a 변")
        b = float_input("b 변")
        if st.button("빗변"):
            st.success(math.sqrt(a*a + b*b))

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 중3 ----------------
elif menu == "중3":
    st.markdown('<div class="section-box">', unsafe_allow_html
