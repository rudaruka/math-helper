import streamlit as st
import sympy as sp
import math
import os

# ======================================================
# 초기 설정
# ======================================================
st.set_page_config(page_title="중등 수학 도우미", layout="wide")

# 세션 상태 초기화: 'menu_key'를 사용하여 강제로 Streamlit 앱을 리렌더링 (다시 시작)하게 만듦
if 'menu_key' not in st.session_state:
    st.session_state['menu_key'] = 0

# ======================================================
# 제목 및 메뉴 설정
# ======================================================
st.markdown("## ✨ 중학생 수학 도우미 — 계산/그래프/공식 한곳에", unsafe_allow_html=True)
st.write("---")

# 학년 선택 함수
def select_grade_menu():
    st.subheader("🎓 학년 선택")
    
    # 학년 선택 셀렉트 박스
    menu = st.selectbox(
        "사용할 학년을 선택하세요 👇",
        ["중1", "중2", "중3"],
        key="grade_selector" # 이 위젯의 상태를 세션에 저장
    )
    
    # 시작 버튼
    if st.button("선택 완료 및 시작"):
        # 선택된 학년으로 이동하기 위해 상태를 업데이트
        st.session_state['selected_grade'] = menu
        st.experimental_rerun() # 전체 앱을 다시 실행하여 선택된 학년 화면으로 이동

# '학년 다시 선택하기' 버튼 클릭 시 실행될 함수
def reset_menu():
    if 'selected_grade' in st.session_state:
        del st.session_state['selected_grade']
    st.session_state['menu_key'] += 1 # 키를 변경하여 강제 리렌더링 유도
    st.experimental_rerun()

# ======================================================
# 공통: 입력 보조 및 심볼
# ======================================================
def float_input(label, value=0.0):
    return st.number_input(label, value=float(value), format="%.5f")

def display_result(label, value):
    st.metric(label=label, value=f"{value}")

x = sp.Symbol('x')
y = sp.Symbol('y')

# ======================================================
# 메인 로직: 선택된 학년에 따라 화면 분기
# ======================================================

# 1. 초기 시작 화면 또는 리셋 후 화면
if 'selected_grade' not in st.session_state:
    select_grade_menu()
    st.stop() # 시작 화면 표시 후 코드 실행 중지

# 2. 학년이 선택된 후 해당 학년의 기능 표시
menu = st.session_state['selected_grade']

# 오른쪽 아래에 '학년 다시 선택하기' 버튼 추가 (컬럼을 사용하여 오른쪽 정렬)
st.sidebar.markdown("---")
if st.sidebar.button("다른 학년 선택하기 🔙", on_click=reset_menu):
    pass # reset_menu 함수가 이미 실행됨

# ======================================================
# 🟦 중1 기능
# (기존 중1 코드와 동일)
# ======================================================
if menu == "중1":
    st.subheader("🟦 중1 수학 도우미")
    
    topic = st.selectbox(
        "단원을 선택하세요 👇",
        [
            "사칙연산 🔢",
            "정수와 유리수 (분수↔소수) ➗",
            "소인수분해 🌲",
            "최대공약수·최소공배수 (GCD·LCM) 🔗",
            "일차방정식 (ax + b = c) ⚖️",
            "좌표평면 (점 사이 거리) 🗺️",
            "도형 — 삼각형·사각형 넓이 📐"
        ]
    )
    
    st.markdown("---")

    # 사칙연산
    if "사칙연산" in topic:
        st.header("🔢 사칙연산")
        col1, col2, col3 = st.columns(3)
        with col1:
            a = float_input("첫 번째 수", 1)
        with col2:
            op = st.selectbox("연산자", ["+", "-", "×", "÷"])
        with col3:
            b = float_input("두 번째 수", 1)
        
        if st.button("계산 결과 보기"):
            result = None
            if op == "+": result = a + b
            elif op == "-": result = a - b
            elif op == "×": result = a * b
            elif op == "÷":
                if b != 0:
                    result = a / b
                else:
                    st.error("❌ 0으로 나눌 수 없습니다.")
                    result = "오류"
            
            if result != "오류" and result is not None:
                display_result(f"{a} {op} {b} =", result)

    # 정수/유리수 관련
    elif "정수와 유리수" in topic:
        st.header("➗ 정수/유리수 정리: 분수 → 소수 변환")
        col1, col2 = st.columns(2)
        with col1:
            num = float_input("분자 (Numerator)")
        with col2:
            den = float_input("분모 (Denominator)", value=1.0)
            
        if st.button("소수 변환"):
            if den == 0: 
                st.error("❌ 분모는 0이 될 수 없습니다.")
            else:
                result_val = num / den
                display_result("변환 결과 (소수)", result_val)
                if result_val == int(result_val):
                    st.info("💡 결과는 정수입니다.")
                elif len(str(result_val).split('.')[-1]) < 10:
                    st.info("💡 결과는 유한소수입니다.")
                else:
                    st.info("💡 결과는 무한소수 (순환소수 또는 비순환소수)일 수 있습니다.")
                

    # 소인수분해
    elif "소인수분해" in topic:
        st.header("🌲 소인수분해")
        n = st.number_input("수를 입력하세요 (양의 정수)", value=12, step=1, min_value=1)
        
        if st.button("소인수분해 실행"):
            try:
                factors = sp.factorint(int(n))
                st.subheader("✅ 소인수분해 결과")
                st.code(f"{n} = {factors}")
                st.success(f"소인수: {list(factors.keys())}")
            except Exception as e:
                st.error(f"❌ 오류: {e}")

    # 최대공약수/최소공배수
    elif "최대공약수·최소공배수" in topic:
        st.header("🔗 최대공약수·최소공배수")
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("첫 번째 수 (a)", value=12, step=1, min_value=1)
        with col2:
            b = st.number_input("두 번째 수 (b)", value=18, step=1, min_value=1)
            
        if st.button("GCD/LCM 계산"):
            gcd_val = math.gcd(int(a), int(b))
            lcm_val = abs(a * b) // math.gcd(int(a), int(b))
            
            col_g, col_l = st.columns(2)
            with col_g:
                st.metric("최대공약수 (GCD)", gcd_val)
            with col_l:
                st.metric("최소공배수 (LCM)", lcm_val)

    # 일차방정식 (ax + b = c)
    elif "일차방정식" in topic:
        st.header("⚖️ 일차방정식 풀이")
        st.info("ℹ️ **SymPy 형식**으로 입력하세요. (예: `2*x + 3 = 11`)")
        eq_text = st.text_input("일차방정식 입력", value="2*x + 3 = 11")
        
        if st.button("방정식 풀기"):
            try:
                eq = sp.Eq(*sp.sympify(eq_text).args)
                solution = sp.solve(eq, x)
                
                st.subheader("✅ 해 (Solution)")
                st.write(f"방정식: ${sp.latex(eq)}$")
                
                if solution:
                    display_result("x =", solution[0])
                else:
                    st.warning("⚠️ 해가 존재하지 않거나 무수히 많습니다.")
            except:
                st.error("❌ 입력 형식을 다시 확인하세요. 변수는 'x'만 사용 가능합니다.")

    # 좌표평면 점 사이 거리
    elif "좌표평면" in topic:
        st.header("🗺️ 좌표평면: 두 점 사이의 거리")
        st.markdown("두 점 $(x_1, y_1)$과 $(x_2, y_2)$ 사이의 거리 $D$는 다음과 같습니다.")
        st.latex(r"D = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📍 점 1")
            x1 = float_input("$x_1$")
            y1 = float_input("$y_1$")
        with col2:
            st.subheader("📍 점 2")
            x2 = float_input("$x_2$")
            y2 = float_input("$y_2$")
            
        if st.button("거리 계산"):
            distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            display_result("두 점 사이의 거리 (D)", f"{distance:.4f}")

    # 도형 넓이
    elif "도형" in topic:
        st.header("📐 도형 넓이 계산")
        shape = st.selectbox("도형 선택", ["삼각형", "직사각형", "평행사변형"])
        
        if shape == "삼각형":
            st.markdown("---")
            st.markdown("### 🔺 삼각형 넓이: $\\frac{1}{2} \\times \\text{밑변} \\times \\text{높이}$")
            col1, col2 = st.columns(2)
            with col1:
                b = float_input("밑변")
            with col2:
                h = float_input("높이")
            if st.button("삼각형 넓이 계산"):
                display_result("넓이", b * h / 2)
                
        elif shape == "직사각형":
            st.markdown("---")
            st.markdown("### ⬛ 직사각형 넓이: $\\text{가로} \\times \\text{세로}$")
            col1, col2 = st.columns(2)
            with col1:
                w = float_input("가로")
            with col2:
                h = float_input("세로")
            if st.button("직사각형 넓이 계산"):
                display_result("넓이", w * h)
                
        else:  # 평행사변형
            st.markdown("---")
            st.markdown("### ▱ 평행사변형 넓이: $\\text{밑변} \\times \\text{높이}$")
            col1, col2 = st.columns(2)
            with col1:
                b = float_input("밑변")
            with col2:
                h = float_input("높이")
            if st.button("평행사변형 넓이 계산"):
                display_result("넓이", b * h)

# ======================================================
# 🟩 중2 기능
# (기존 중2 코드와 동일)
# ======================================================
elif menu == "중2":
    st.subheader("🟩 중2 수학 도우미")

    topic = st.selectbox(
        "단원 선택 👇",
        [
            "식의 계산 (전개/인수분해) 📝",
            "연립방정식 (미지수 2개) 🎯",
            "일차함수 y=ax+b (값 계산) 📈",
            "일차함수 그래프 (y=f(x)) 📊",
            "유리수·순환소수 (분수↔소수) ➗",
            "도형 — 원 넓이/호의 길이 🔵"
        ]
    )
    
    st.markdown("---")

    # 식의 계산 (인수분해/전개)
    if "식의 계산" in topic:
        st.header("📝 식의 계산 (다항식)")
        st.info("ℹ️ **SymPy 형식**으로 입력하세요. (예: `(x+3)*(x-2)` 또는 `x**2 - x - 6`)")
        expr = st.text_input("식 입력", value="(x+3)*(x-2)")
        mode = st.radio("기능 선택", ["전개 (Expand)", "인수분해 (Factor)"])
        
        if st.button("실행"):
            try:
                e = sp.sympify(expr)
                if "전개" in mode:
                    result = sp.expand(e)
                    st.subheader("✅ 전개 결과")
                else:
                    result = sp.factor(e)
                    st.subheader("✅ 인수분해 결과")
                
                st.latex(sp.latex(result))
                st.code(str(result))
            except:
                st.error("❌ 식 형식을 확인하세요. 변수는 'x'만 사용 가능합니다.")

    # 연립방정식
    elif "연립방정식" in topic:
        st.header("🎯 연립방정식 풀이 (미지수 x, y)")
        st.info("ℹ️ **SymPy 형식**으로 입력하세요. (예: `2*x + y - 7` (우변 0 가정))")
        
        eq1 = st.text_input("1번 식", value="2*x + y - 7")
        eq2 = st.text_input("2번 식", value="x - y - 1")
        
        if st.button("연립방정식 풀기"):
            try:
                sol = sp.solve([eq1, eq2], [x, y])
                
                st.subheader("✅ 해 (Solution)")
                if sol:
                    st.write(f"$$x = {sp.latex(sol[x])}$$")
                    st.write(f"$$y = {sp.latex(sol[y])}$$")
                    st.success(f"해: x={sol[x]}, y={sol[y]}")
                else:
                    st.warning("⚠️ 해가 존재하지 않거나 무수히 많습니다.")
            except:
                st.error("❌ 입력 형식을 확인하세요. 변수는 'x', 'y'만 사용 가능합니다. 식의 우변이 0이라고 가정하고 좌변만 입력해도 됩니다.")

    # 일차함수 계산
    elif "일차함수 y=ax+b" in topic:
        st.header("📈 일차함수 값 계산")
        st.markdown("함수: $y = ax + b$")
        
        col_a, col_b, col_x = st.columns(3)
        with col_a:
            a = float_input("기울기 (a)")
        with col_b:
            b = float_input("y절편 (b)")
        with col_x:
            xv = float_input("x 값")
            
        if st.button("y 계산"):
            result = a * xv + b
            display_result(f"y = {a}*({xv}) + {b} =", result)
            
    # 일차함수 그래프
    elif "일차함수 그래프" in topic:
        st.header("📊 일차함수 그래프 그리기")
        st.info("ℹ️ **함수식의 우변만 SymPy 형식**으로 입력하세요. (예: `2*x + 3`)")
        func = st.text_input("함수식 입력 (y = ...)", value="2*x + 3")
        
        if st.button("그래프 그리기"):
            img_file = "g.png"
            try:
                f = sp.sympify(func)
                p = sp.plot(f, (x, -10, 10), show=False, title=f"y = {func}")
                p.save(img_file)
                st.image(img_file, caption=f"일차함수 $y = {sp.latex(f)}$")
            except:
                st.error("❌ 식 형식을 확인하세요. 변수는 'x'만 사용 가능합니다.")
            finally:
                if os.path.exists(img_file):
                    os.remove(img_file)

    # 순환소수 변환
    elif "유리수·순환소수" in topic:
        st.header("➗ 분수 → 소수 변환")
        
        col1, col2 = st.columns(2)
        with col1:
            num = float_input("분자", 1)
        with col2:
            den = float_input("분모", 3)
            
        if st.button("변환 결과 보기"):
            if den == 0:
                st.error("❌ 분모는 0이 될 수 없습니다.")
            else:
                result = num / den
                display_result("소수", f"{result:.10f}...")
                st.info("💡 순환마디를 찾는 것은 계산이 복잡하므로, 계산기로 확인해 보세요.")
                
    # 원 넓이 / 호의 길이
    elif "도형 — 원 넓이/호의 길이" in topic:
        st.header("🔵 원의 넓이 및 부채꼴 호의 길이")

        r = float_input("반지름 (r)")
        
        st.subheader("부채꼴 계산")
        ang = float_input("중심각 (도, $\\theta$) (원 전체는 360)")
        
        if st.button("계산"):
            area_circle = math.pi * r * r
            arc_length = 2 * math.pi * r * (ang / 360)
            
            st.markdown("---")
            col_a, col_l = st.columns(2)
            with col_a:
                st.metric("원 전체 넓이 ($r^2 \pi$)", f"{area_circle:.4f} ($\pi$를 곱한 값)")
            with col_l:
                st.metric("호의 길이 ($2 r \pi \\times \\frac{\\theta}{360}$)", f"{arc_length:.4f} ($\pi$를 곱한 값)")
            st.write(f"**원 둘레** $2 \pi r$ = ${2 * math.pi * r:.4f}$")

# ======================================================
# 🟥 중3 기능
# (기존 중3 코드와 동일)
# ======================================================
elif menu == "중3":
    st.subheader("🟥 중3 수학 도우미")

    topic = st.selectbox(
        "단원 선택 👇",
        [
            "이차방정식 (해 구하기) 💣",
            "이차함수 y=ax^2+bx+c (값 계산) 📊",
            "이차함수 그래프 (포물선) 📉",
            "피타고라스 정리 (직각삼각형) 📐",
            "삼각비 (sin, cos, tan) 📏",
            "확률 (경우의 수) 🎲"
        ]
    )
    
    st.markdown("---")

    # 이차방정식
    if "이차방정식" in topic:
        st.header("💣 이차방정식 풀이")
        st.info("ℹ️ **SymPy 형식**으로 입력하세요. (예: `x**2 - 5*x + 6`) (우변 0 가정)")
        eq = st.text_input("이차방정식 좌변 입력", value="x**2 - 5*x + 6")
        
        if st.button("해 구하기"):
            try:
                e = sp.sympify(eq)
                solution = sp.solve(e, x)
                
                st.subheader("✅ 해 (Solution)")
                st.write(f"방정식: ${sp.latex(sp.Eq(e, 0))}$")
                
                if solution:
                    for i, sol in enumerate(solution):
                         st.markdown(f"**해 {i+1}**: ${sp.latex(sol)}$")
                    st.success(f"해: {solution}")
                else:
                    st.warning("⚠️ 실수해가 존재하지 않을 수 있습니다. (판별식 D < 0)")
            except:
                st.error("❌ 식 형식을 다시 확인하세요. 변수는 'x'만 사용 가능합니다.")

    # 이차함수 계산
    elif "이차함수 y=ax^2+bx+c" in topic:
        st.header("📊 이차함수 값 계산")
        st.markdown("함수: $y = ax^2 + bx + c$")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            a = float_input("a")
        with col_b:
            b = float_input("b")
        with col_c:
            c = float_input("c")
            
        xv = float_input("x 값")
        
        if st.button("y 계산"):
            result = a * xv * xv + b * xv + c
            display_result(f"y = {a}({xv})^2 + {b}({xv}) + {c} =", result)

    # 그래프
    elif "이차함수 그래프" in topic:
        st.header("📉 이차함수 그래프 (포물선) 그리기")
        st.info("ℹ️ **함수식의 우변만 SymPy 형식**으로 입력하세요. (예: `x**2 - 4*x + 3`)")
        func = st.text_input("함수식 입력 (y = ...)", value="x**2 - 4*x + 3")
        
        if st.button("그래프 그리기"):
            img_file = "quad.png"
            try:
                f = sp.sympify(func)
                p = sp.plot(f, (x, -10, 10), show=False, title=f"y = {func}")
                p.save(img_file)
                st.image(img_file, caption=f"이차함수 $y = {sp.latex(f)}$")
            except:
                st.error("❌ 식 형식을 다시 확인하세요. 변수는 'x'만 사용 가능합니다.")
            finally:
                if os.path.exists(img_file):
                    os.remove(img_file)


    # 피타고라스
    elif "피타고라스 정리" in topic:
        st.header("📐 피타고라스 정리")
        st.markdown("직각삼각형의 두 변 $a, b$가 주어졌을 때 빗변 $c$의 길이:")
        st.latex(r"a^2 + b^2 = c^2 \implies c = \sqrt{a^2 + b^2}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            a = float_input("a 변")
        with col_b:
            b = float_input("b 변")
            
        if st.button("빗변 c 계산"):
            c = math.sqrt(a * a + b * b)
            display_result("빗변 (c)", f"{c:.4f}")

    # 삼각비
    elif "삼각비" in topic:
        st.header("📏 삼각비 (sin, cos, tan)")
        st.markdown("각도 $\\theta$에 대한 삼각비 값을 계산합니다.")
        
        ang = float_input("각도(도 단위)")
        
        if st.button("계산"):
            r = math.radians(ang)
            
            st.markdown("---")
            col_s, col_c, col_t = st.columns(3)
            with col_s:
                st.metric("sin", f"{math.sin(r):.4f}")
            with col_c:
                st.metric("cos", f"{math.cos(r):.4f}")
            with col_t:
                st.metric("tan", f"{math.tan(r):.4f}")

    # 확률
    elif "확률" in topic:
        st.header("🎲 확률 계산")
        st.markdown("확률 $P = \\frac{\\text{좋은 경우의 수}}{\\text{전체 경우의 수}}$")
        
        col_g, col_t = st.columns(2)
        with col_g:
            good = st.number_input("좋은 경우의 수", value=1, step=1, min_value=0)
        with col_t:
            total = st.number_input("전체 경우의 수", value=6, step=1, min_value=1)
            
        if st.button("확률 계산"):
            if total != 0 and good <= total:
                probability = good / total
                display_result("확률 (소수)", f"{probability:.4f}")
                st.metric("확률 (%)", f"{probability*100:.2f}%")
            elif total == 0:
                st.error("❌ 전체 경우의 수는 0이 될 수 없습니다.")
            elif good > total:
                st.error("❌ 좋은 경우의 수가 전체 경우의 수보다 클 수 없습니다.")
