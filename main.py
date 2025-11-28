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

st.title("🧮 다기능 계산기")
st.write("사칙연산, 모듈러 연산, 지수 연산, 로그 연산을 한 곳에서 계산해 보세요.")

# 사이드바에서 기능 선택
mode = st.sidebar.radio(
    "계산 기능 선택",
    ("사칙연산", "모듈러 연산", "지수 연산", "로그 연산")
)

# -----------------------------------
# 1. 사칙연산 계산기
# -----------------------------------
if mode == "사칙연산":
    st.header("➕ 사칙연산 계산기")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("첫 번째 수 (a)", value=0.0, format="%.6f")
    with col2:
        b = st.number_input("두 번째 수 (b)", value=0.0, format="%.6f")

    op = st.radio(
        "연산 선택",
        ("더하기 (a + b)", "빼기 (a - b)", "곱하기 (a × b)", "나누기 (a ÷ b)")
    )

    if st.button("계산하기", key="basic_calc"):
        if op == "더하기 (a + b)":
            result = a + b
            st.success(f"결과: {a} + {b} = {result}")
        elif op == "빼기 (a - b)":
            result = a - b
            st.success(f"결과: {a} - {b} = {result}")
        elif op == "곱하기 (a × b)":
            result = a * b
            st.success(f"결과: {a} × {b} = {result}")
        elif op == "나누기 (a ÷ b)":
            if b == 0:
                st.error("0으로는 나눌 수 없습니다. (b ≠ 0)")
            else:
                result = a / b
                st.success(f"결과: {a} ÷ {b} = {result}")

# -----------------------------------
# 2. 모듈러 연산 계산기
# -----------------------------------
elif mode == "모듈러 연산":
    st.header("🔢 모듈러 연산 계산기 (a mod n)")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("피제수 (a)", value=0, step=1)
    with col2:
        n = st.number_input("법 (n, 양의 정수)", value=1, step=1, min_value=1)

    st.caption("※ 정수 연산을 권장합니다. (소수로 입력해도 내부에서 정수로 변환하지는 않습니다)")

    if st.button("계산하기", key="mod_calc"):
        if n == 0:
            st.error("법 n은 0이 될 수 없습니다.")
        else:
            # 파이썬의 %는 음수도 처리 가능하지만, 여기서는 일반적인 의미로 안내
            result = a % n
            st.success(f"결과: {a} mod {n} = {result}")

# -----------------------------------
# 3. 지수 연산 계산기
# -----------------------------------
elif mode == "지수 연산":
    st.header("📈 지수 연산 계산기 (a^b)")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("밑 (a)", value=2.0, format="%.6f")
    with col2:
        b = st.number_input("지수 (b)", value=3.0, format="%.6f")

    st.caption("※ a^b 형태의 지수 연산을 계산합니다.")

    if st.button("계산하기", key="exp_calc"):
        try:
            result = a ** b
            st.success(f"결과: {a} ^ {b} = {result}")
        except OverflowError:
            st.error("값이 너무 커서 계산할 수 없습니다.")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")

# -----------------------------------
# 4. 로그 연산 계산기
# -----------------------------------
elif mode == "로그 연산":
    st.header("📉 로그 연산 계산기 (log₍b₎(x))")

    x = st.number_input("진수 (x, x > 0)", value=10.0, format="%.6f")
    base_type = st.radio(
        "로그 종류 선택",
        ("상용로그 (log₁₀ x)", "자연로그 (ln x)", "밑을 내가 정하기")
    )

    custom_base = None
    if base_type == "밑을 내가 정하기":
        custom_base = st.number_input("밑 (b, b > 0, b ≠ 1)", value=2.0, format="%.6f")

    if st.button("계산하기", key="log_calc"):
        if x <= 0:
            st.error("진수 x는 0보다 커야 합니다.")
        else:
            try:
                if base_type == "상용로그 (log₁₀ x)":
                    result = math.log10(x)
                    st.success(f"결과: log₁₀({x}) = {result}")
                elif base_type == "자연로그 (ln x)":
                    result = math.log(x)
                    st.success(f"결과: ln({x}) = {result}")
                else:
                    if custom_base is None:
                        st.error("밑 b를 입력해 주세요.")
                    elif custom_base <= 0 or custom_base == 1:
                        st.error("밑 b는 0보다 크고 1이 아니어야 합니다.")
                    else:
                        # 밑이 b인 로그: log_b(x) = ln(x) / ln(b)
                        result = math.log(x) / math.log(custom_base)
                        st.success(f"결과: log₍{custom_base}₎({x}) = {result}")
            except ValueError:
                st.error("로그를 계산할 수 없는 입력입니다.")
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
