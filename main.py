import math
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="다기능 수학 계산기",
    page_icon="🧮",
    layout="centered",
)

st.title("🧮 다기능 수학 계산기")
st.write("사칙연산, 모듈러 연산, 지수 연산, 로그 연산을 할 수 있는 웹 계산기입니다.")

# -----------------------------
# 사이드바: 연산 종류 선택
# -----------------------------
st.sidebar.header("연산 종류 선택")
mode = st.sidebar.radio(
    "사용할 계산 기능을 선택하세요.",
    ("사칙연산", "모듈러 연산", "지수 연산", "로그 연산")
)

st.sidebar.info("👈 왼쪽에서 기능을 선택하고, 화면에서 값을 입력한 뒤 계산 버튼을 눌러보세요.")


# -----------------------------
# 1. 사칙연산
# -----------------------------
if mode == "사칙연산":
    st.subheader("➕➖✖️➗ 사칙연산")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("첫 번째 수 (a)", value=0.0, format="%.6f")
    with col2:
        b = st.number_input("두 번째 수 (b)", value=0.0, format="%.6f")

    op = st.selectbox(
        "연산자를 선택하세요.",
        ("+", "-", "×", "÷")
    )

    if st.button("사칙연산 계산하기"):
        try:
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "×":
                result = a * b
            elif op == "÷":
                if b == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    result = None
                else:
                    result = a / b
            else:
                result = None

            if result is not None:
                st.success(f"결과: {a} {op} {b} = {result}")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")


# -----------------------------
# 2. 모듈러 연산
# -----------------------------
elif mode == "모듈러 연산":
    st.subheader("♻️ 모듈러 연산 (a mod n)")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("피제수 (a)", value=0, step=1)
    with col2:
        n = st.number_input("법(mod) n", value=1, step=1, min_value=1)

    st.caption("※ 모듈러 연산은 보통 정수에 대해 정의되므로, 여기서는 정수 입력을 권장합니다.")

    if st.button("모듈러 연산 계산하기"):
        try:
            # 정수로 강제 변환 (필요 없으면 이 부분 제거 가능)
            a_int = int(a)
            n_int = int(n)

            if n_int == 0:
                st.error("법 n이 0일 수는 없습니다.")
            else:
                result = a_int % n_int
                st.success(f"결과: {a_int} mod {n_int} = {result}")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")


# -----------------------------
# 3. 지수 연산
# -----------------------------
elif mode == "지수 연산":
    st.subheader("⬆️ 지수 연산 (a^b)")

    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("밑 (a)", value=2.0, format="%.6f")
    with col2:
        exp = st.number_input("지수 (b)", value=3.0, format="%.6f")

    if st.button("지수 연산 계산하기"):
        try:
            result = base ** exp
            st.success(f"결과: {base} ^ {exp} = {result}")
        except OverflowError:
            st.error("값이 너무 커서 계산할 수 없습니다. (OverflowError)")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")


# -----------------------------
# 4. 로그 연산
# -----------------------------
elif mode == "로그 연산":
    st.subheader("📉 로그 연산")

    st.write("로그의 밑과 진수(값)를 입력하고 로그 값을 계산합니다.")

    value = st.number_input("진수 (log₍base₎(value)에서 value)", value=10.0, format="%.6f", min_value=0.0)
    base_option = st.radio(
        "밑 선택",
        ("상용로그 (밑 10)", "자연로그 (밑 e)", "사용자 지정 밑")
    )

    if base_option == "사용자 지정 밑":
        base = st.number_input("밑 (base)", value=2.0, format="%.6f")
    elif base_option == "상용로그 (밑 10)":
        base = 10
    else:  # 자연로그
        base = math.e

    if st.button("로그 계산하기"):
        try:
            if value <= 0:
                st.error("로그의 진수는 0보다 커야 합니다.")
            elif base <= 0 or base == 1:
                st.error("로그의 밑은 0보다 크고 1이 아니어야 합니다.")
            else:
                # 로그 밑 변경 공식 사용: log_base(value) = ln(value) / ln(base)
                result = math.log(value) / math.log(base)
                if base_option == "자연로그 (밑 e)":
                    st.success(f"결과: ln({value}) = {result}")
                elif base_option == "상용로그 (밑 10)":
                    st.success(f"결과: log₁₀({value}) = {result}")
                else:
                    st.success(f"결과: log₍{base}₎({value}) = {result}")
        except ValueError:
            st.error("입력값이 로그의 정의역을 벗어났습니다.")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")
