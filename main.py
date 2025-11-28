import math
import streamlit as st

# -----------------------------------
# 기본 설정
# -----------------------------------
st.set_page_config(
    page_title="다기능 계산기",
    page_icon="🧮",
    layout="centered"
)

# -----------------------------------
# 커스텀 CSS - 계산기 스타일
# -----------------------------------
st.markdown(
    """
    <style>
    /* 전체 배경 */
    .main {
        background: radial-gradient(circle at top, #f5f7ff 0, #e4e7f5 40%, #dde1f0 100%);
    }

    /* 제목 위치 중앙 정렬 */
    .center-title {
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .center-subtitle {
        text-align: center;
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 1.5rem;
    }

    /* 계산기 카드 */
    .calculator-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 1.5rem 1.5rem 1.8rem 1.5rem;
        background: linear-gradient(145deg, #1f2933, #111827);
        border-radius: 24px;
        box-shadow:
            0 14px 28px rgba(0, 0, 0, 0.35),
            0 10px 10px rgba(0, 0, 0, 0.30);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* 디스플레이 영역 */
    .calc-display {
        background: radial-gradient(circle at top left, #4b5563 0, #020617 65%);
        border-radius: 18px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        min-height: 70px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: #e5e7eb;
        box-shadow: inset 0 0 8px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.12);
    }
    .calc-display-label {
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 0.1rem;
    }
    .calc-display-value {
        font-size: 1.3rem;
        font-weight: 600;
        text-align: right;
        font-family: "SF Mono", ui-monospace, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        word-wrap: break-word;
    }

    /* 모드 표시 */
    .calc-mode-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: rgba(15,118,110,0.18);
        color: #a5f3fc;
        border: 1px solid rgba(45,212,191,0.5);
        margin-bottom: 0.4rem;
    }

    /* 세부 설정 카드 느낌 */
    .calc-section {
        background: rgba(15,23,42,0.9);
        border-radius: 18px;
        padding: 0.9rem 0.9rem 0.7rem 0.9rem;
        border: 1px solid rgba(148,163,184,0.3);
        margin-top: 0.3rem;
    }
    .calc-section-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e5e7eb;
        margin-bottom: 0.2rem;
    }
    .calc-section-caption {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }

    /* Streamlit 기본 위젯 폰트/색 조정 약간 */
    .stNumberInput>label, .stRadio>label, .stTextInput>label {
        font-size: 0.8rem !important;
        color: #e5e7eb !important;
    }
    .stRadio div[role="radiogroup"] > label {
        font-size: 0.8rem !important;
    }

    /* 사이드바 살짝 다듬기 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0b1220 60%, #020617 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    /* 버튼 넓이 */
    .stButton>button {
        width: 100%;
        border-radius: 999px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.8rem;
        padding: 0.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# 세션 상태: 디스플레이 표현
# -----------------------------------
if "display_text" not in st.session_state:
    st.session_state.display_text = "0"

# -----------------------------------
# 제목
# -----------------------------------
st.markdown('<h1 class="center-title">🧮 Multi Calculator</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="center-subtitle">사칙연산 · 모듈러 · 지수 · 로그를 하나의 계산기에서!</div>',
    unsafe_allow_html=True
)

# 사이드바에서 기능 선택
mode = st.sidebar.radio(
    "계산 모드 선택",
    ("사칙연산", "모듈러 연산", "지수 연산", "로그 연산")
)

# -----------------------------------
# 계산기 카드 시작
# -----------------------------------
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# 디스플레이 영역
st.markdown(
    f"""
    <div class="calc-display">
        <div class="calc-display-label">RESULT</div>
        <div class="calc-display-value">{st.session_state.display_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# 모드 태그
st.markdown(f'<div class="calc-mode-tag">{mode}</div>', unsafe_allow_html=True)

# -----------------------------------
# 1. 사칙연산
# -----------------------------------
if mode == "사칙연산":
    st.markdown(
        """
        <div class="calc-section">
            <div class="calc-section-title">사칙연산 설정</div>
            <div class="calc-section-caption">두 수를 입력하고 원하는 연산을 선택하세요.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("첫 번째 수 (a)", value=0.0, format="%.6f", key="basic_a")
        with col2:
            b = st.number_input("두 번째 수 (b)", value=0.0, format="%.6f", key="basic_b")

        op = st.radio(
            "연산 선택",
            ("더하기 (a + b)", "빼기 (a - b)", "곱하기 (a × b)", "나누기 (a ÷ b)"),
            horizontal=True
        )

        if st.button("계산하기", key="basic_calc"):
            if op == "더하기 (a + b)":
                result = a + b
                expr = f"{a} + {b} = {result}"
            elif op == "빼기 (a - b)":
                result = a - b
                expr = f"{a} - {b} = {result}"
            elif op == "곱하기 (a × b)":
                result = a * b
                expr = f"{a} × {b} = {result}"
            else:  # 나누기
                if b == 0:
                    st.error("0으로는 나눌 수 없습니다. (b ≠ 0)")
                    expr = "Error: divide by 0"
                else:
                    result = a / b
                    expr = f"{a} ÷ {b} = {result}"

            st.session_state.display_text = expr
            st.rerun()

# -----------------------------------
# 2. 모듈러 연산
# -----------------------------------
elif mode == "모듈러 연산":
    st.markdown(
        """
        <div class="calc-section">
            <div class="calc-section-title">모듈러 연산 설정</div>
            <div class="calc-section-caption">a mod n 형태의 연산을 계산합니다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("피제수 (a)", value=0, step=1, key="mod_a")
        with col2:
            n = st.number_input("법 (n, 양의 정수)", value=1, step=1, min_value=1, key="mod_n")

        st.caption("※ 정수 입력을 권장합니다. (파이썬의 % 규칙을 그대로 사용합니다.)")

        if st.button("계산하기", key="mod_calc"):
            if n == 0:
                st.error("법 n은 0이 될 수 없습니다.")
                expr = "Error: n = 0"
            else:
                result = a % n
                expr = f"{a} mod {n} = {result}"

            st.session_state.display_text = expr
            st.rerun()

# -----------------------------------
# 3. 지수 연산
# -----------------------------------
elif mode == "지수 연산":
    st.markdown(
        """
        <div class="calc-section">
            <div class="calc-section-title">지수 연산 설정</div>
            <div class="calc-section-caption">a^b 형태의 지수 연산을 계산합니다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("밑 (a)", value=2.0, format="%.6f", key="exp_a")
        with col2:
            b = st.number_input("지수 (b)", value=3.0, format="%.6f", key="exp_b")

        if st.button("계산하기", key="exp_calc"):
            try:
                result = a ** b
                expr = f"{a} ^ {b} = {result}"
            except OverflowError:
                st.error("값이 너무 커서 계산할 수 없습니다.")
                expr = "Error: overflow"
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
                expr = "Error"

            st.session_state.display_text = expr
            st.rerun()

# -----------------------------------
# 4. 로그 연산
# -----------------------------------
elif mode == "로그 연산":
    st.markdown(
        """
        <div class="calc-section">
            <div class="calc-section-title">로그 연산 설정</div>
            <div class="calc-section-caption">상용로그, 자연로그, 임의의 밑 로그를 계산합니다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        x = st.number_input("진수 (x, x > 0)", value=10.0, format="%.6f", key="log_x")

        base_type = st.radio(
            "로그 종류 선택",
            ("상용로그 (log₁₀ x)", "자연로그 (ln x)", "밑을 내가 정하기"),
            horizontal=False
        )

        custom_base = None
        if base_type == "밑을 내가 정하기":
            custom_base = st.number_input("밑 (b, b > 0, b ≠ 1)", value=2.0, format="%.6f", key="log_b")

        if st.button("계산하기", key="log_calc"):
            if x <= 0:
                st.error("진수 x는 0보다 커야 합니다.")
                expr = "Error: x ≤ 0"
            else:
                try:
                    if base_type == "상용로그 (log₁₀ x)":
                        result = math.log10(x)
                        expr = f"log₁₀({x}) = {result}"
                    elif base_type == "자연로그 (ln x)":
                        result = math.log(x)
                        expr = f"ln({x}) = {result}"
                    else:
                        if custom_base is None:
                            st.error("밑 b를 입력해 주세요.")
                            expr = "Error: no base"
                        elif custom_base <= 0 or custom_base == 1:
                            st.error("밑 b는 0보다 크고 1이 아니어야 합니다.")
                            expr = "Error: invalid base"
                        else:
                            result = math.log(x) / math.log(custom_base)
                            expr = f"log₍{custom_base}₎({x}) = {result}"
                except ValueError:
                    st.error("로그를 계산할 수 없는 입력입니다.")
                    expr = "Error: invalid input"
                except Exception as e:
                    st.error(f"계산 중 오류가 발생했습니다: {e}")
                    expr = "Error"

            st.session_state.display_text = expr
            st.rerun()

# 계산기 카드 끝
st.markdown('</div>', unsafe_allow_html=True)
