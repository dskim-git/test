import math
import random

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------
# 기본 설정
# -----------------------------------
st.set_page_config(
    page_title="다기능 수학 웹앱",
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
# 세션 상태: 계산기 디스플레이 텍스트
# -----------------------------------
if "display_text" not in st.session_state:
    st.session_state.display_text = "0"

# -----------------------------------
# 사이드바: 앱 선택
# -----------------------------------
st.sidebar.title("🧮 수학 웹앱")
app_mode = st.sidebar.radio(
    "사용할 앱 선택",
    ("계산기", "확률 시뮬레이터", "연도별 세계인구 분석")
)

# -----------------------------------
# 공통 상단 제목
# -----------------------------------
st.markdown('<h1 class="center-title">🧮 Multi Math App</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="center-subtitle">계산기 · 확률 시뮬레이터 · 세계 인구 분석</div>',
    unsafe_allow_html=True
)

# =============================================================================
# 0. 데이터 로딩 함수 (세계 인구)
# =============================================================================
@st.cache_data
def load_world_population():
    # main.py와 같은 폴더에 있는 world_population.csv 사용
    df = pd.read_csv("world_population.csv")
    return df

# =============================================================================
# 1. 계산기 앱
# =============================================================================
if app_mode == "계산기":

    # 계산기 내부 모드 (사칙/모듈러/지수/로그)
    calc_mode = st.sidebar.radio(
        "계산 모드 선택",
        ("사칙연산", "모듈러 연산", "지수 연산", "로그 연산")
    )

    # 계산기 카드 시작
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
    st.markdown(f'<div class="calc-mode-tag">{calc_mode}</div>', unsafe_allow_html=True)

    # -------------------------------
    # 1-1. 사칙연산
    # -------------------------------
    if calc_mode == "사칙연산":
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

    # -------------------------------
    # 1-2. 모듈러 연산
    # -------------------------------
    elif calc_mode == "모듈러 연산":
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

    # -------------------------------
    # 1-3. 지수 연산
    # -------------------------------
    elif calc_mode == "지수 연산":
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

    # -------------------------------
    # 1-4. 로그 연산
    # -------------------------------
    elif calc_mode == "로그 연산":
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
            expr = ""
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

# =============================================================================
# 2. 확률 시뮬레이터 앱
# =============================================================================
elif app_mode == "확률 시뮬레이터":
    st.subheader("🎲 확률 시뮬레이터")

    st.markdown(
        """
        동전 또는 주사위를 선택하고 시행 횟수를 정한 뒤<br>
        시뮬레이션을 실행하면 **실제 상대도수**를 Plotly 그래프로 볼 수 있습니다.
        """,
        unsafe_allow_html=True
    )

    # 실험 설정
    col_exp, col_n = st.columns(2)
    with col_exp:
        experiment = st.radio(
            "실험 종류",
            ("동전 던지기", "주사위 던지기")
        )
    with col_n:
        n_trials = st.number_input(
            "시행 횟수",
            min_value=1,
            max_value=100000,
            value=1000,
            step=100
        )

    run = st.button("시뮬레이션 실행하기")

    if run:
        results = []

        # -----------------------------
        # 동전 던지기 시뮬레이션
        # -----------------------------
        if experiment == "동전 던지기":
            for _ in range(n_trials):
                outcome = random.choice(["앞면", "뒷면"])
                results.append(outcome)

            df = pd.DataFrame({"결과": results})
            freq = df["결과"].value_counts().reset_index()
            freq.columns = ["결과", "도수"]
            freq["상대도수"] = freq["도수"] / n_trials

            fig = px.bar(
                freq,
                x="결과",
                y="상대도수",
                text=freq["상대도수"].map(lambda x: f"{x:.3f}")
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_title="상대도수",
                xaxis_title="결과",
                title=f"동전 던지기 상대도수 (시행 횟수: {n_trials})"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(freq)

            st.info("이론적으로는 앞면과 뒷면의 확률이 각각 0.5에 가깝게 나타나야 합니다.")

        # -----------------------------
        # 주사위 던지기 시뮬레이션
        # -----------------------------
        else:  # "주사위 던지기"
            for _ in range(n_trials):
                outcome = random.randint(1, 6)
                results.append(outcome)

            df = pd.DataFrame({"결과": results})
            freq = df["결과"].value_counts().sort_index().reset_index()
            freq.columns = ["결과", "도수"]
            freq["상대도수"] = freq["도수"] / n_trials

            fig = px.bar(
                freq,
                x="결과",
                y="상대도수",
                text=freq["상대도수"].map(lambda x: f"{x:.3f}")
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_title="상대도수",
                xaxis_title="눈",
                title=f"주사위 눈의 상대도수 (시행 횟수: {n_trials})"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(freq)

            st.info("이론적으로는 1~6의 각 눈이 모두 확률 1/6 ≈ 0.167 에 가깝게 나타나야 합니다.")

# =============================================================================
# 3. 연도별 세계인구 분석 앱
# =============================================================================
elif app_mode == "연도별 세계인구 분석":
    st.subheader("🌍 연도별 세계 인구 분석")

    st.markdown(
        """
        `world_population.csv` 데이터를 이용해서<br>
        **연도별 세계 인구 분포**와 **세계 인구 비율(%)**을<br>
        Plotly 세계지도에서 시각화합니다.
        """,
        unsafe_allow_html=True
    )

    df_pop = load_world_population()

    # 사용할 연도들 (CSV 컬럼: 1970, 1980, ..., 2022)
    year_list = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

    # 🔹 슬라이드바 형태로 연도 선택 (select_slider 사용)
    year = st.select_slider("연도 선택", options=year_list, value=2022)

    st.markdown("---")

    # -----------------------------
    # 3-1. 해당 연도의 인구수 지도 (구간 색칠)
    # -----------------------------
    st.markdown(f"### 🗺 {year}년 세계 인구 분포 (구간별 색칠)")

    pop_col = str(year)  # CSV에서 연도 컬럼 이름이 '1970', '1980', ... 형태라고 가정
    if pop_col not in df_pop.columns:
        st.error(f"데이터에 `{pop_col}` 컬럼이 없습니다. CSV 컬럼명을 확인하세요.")
    else:
        df_map = df_pop.copy()

        # 인구수 구간 설정 (대략적인 구간)
        bins_pop = [0, 1e7, 5e7, 1e8, 5e8, 2e9]
        labels_pop = ["< 10M", "10M–50M", "50M–100M", "100M–500M", "≥ 500M"]

        df_map["Population Range"] = pd.cut(
            df_map[pop_col],
            bins=bins_pop,
            labels=labels_pop,
            include_lowest=True
        )

        fig_pop = px.choropleth(
            df_map,
            locations="code",              # 3자리 국가 코드 (예: USA, KOR)
            color="Population Range",
            hover_name="Country",
            hover_data={pop_col: ":,"},
            category_orders={"Population Range": labels_pop},
            title=f"{year}년 세계 인구 (구간별 인구수)"
        )
        fig_pop.update_layout(
            legend_title_text="인구수 구간",
        )

        st.plotly_chart(fig_pop, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # 3-2. 세계 인구 비율(%) 기준 지도
    # -----------------------------
    st.markdown("### 🌎 세계 인구 비율(%)에 따른 구간 색칠")

    if "World Population Percentage" not in df_pop.columns:
        st.error("데이터에 'World Population Percentage' 컬럼이 없습니다.")
    else:
        df_pct = df_pop.copy()

        # world population percentage 구간 (값은 % 단위)
        bins_pct = [0, 0.05, 0.1, 0.5, 1, 3, 10, 25]
        labels_pct = [
            "< 0.05%",
            "0.05–0.1%",
            "0.1–0.5%",
            "0.5–1%",
            "1–3%",
            "3–10%",
            "≥ 10%"
        ]

        df_pct["World Pop Share Range"] = pd.cut(
            df_pct["World Population Percentage"],
            bins=bins_pct,
            labels=labels_pct,
            include_lowest=True
        )

        fig_pct = px.choropleth(
            df_pct,
            locations="code",
            color="World Pop Share Range",
            hover_name="Country",
            hover_data={"World Population Percentage": True},
            category_orders={"World Pop Share Range": labels_pct},
            title="세계 인구에서 각 국가가 차지하는 비율(%) 구간"
        )
        fig_pct.update_layout(
            legend_title_text="세계 인구 비율 구간"
        )

        st.plotly_chart(fig_pct, use_container_width=True)

        st.caption(
            "※ World Population Percentage 값은 각 나라 인구가 전체 세계 인구에서 차지하는 비율(%)입니다."
        )
