# app_mbti.py
import streamlit as st
from agents import run_mbti_crew

st.set_page_config(
    page_title="MBTI 짝궁 찾기",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 나의 MBTI + 짝궁 찾기")
st.caption("20개 질문으로 MBTI를 진단하고 최적의 짝궁을 찾아드립니다")

questions = [
    # E/I
    "파티에서 처음 보는 사람에게 먼저 말을 건다",
    "주말에 친구들과 어울리면 에너지가 충전된다",
    "혼자 있는 시간이 불편하다",
    "여러 사람과 함께 일할 때 더 효율적이다",
    "생각보다 말이 먼저 나오는 편이다",
    # S/N
    "미래 가능성보다 현재 사실이 더 중요하다",
    "상상력보다 경험을 더 신뢰한다",
    "새로운 아이디어보다 검증된 방법을 선호한다",
    "세부사항을 꼼꼼히 따지는 편이다",
    "현실적인 계획이 창의적인 비전보다 낫다",
    # T/F
    "결정할 때 감정보다 논리를 따른다",
    "상대방이 틀리면 바로 지적하는 편이다",
    "공정함이 배려보다 중요하다",
    "칭찬보다 정확한 피드백이 더 도움이 된다",
    "친구가 힘들다고 할 때 해결책을 먼저 찾는다",
    # J/P
    "여행 전 세부 일정을 미리 짠다",
    "마감일 전에 여유있게 끝내는 편이다",
    "정해진 루틴이 있어야 편하다",
    "즉흥적인 변화보다 계획된 일정을 선호한다",
    "할 일 목록을 만들고 체크하는 걸 좋아한다",
]

sections = (
    ["🔋 에너지 방향 (E/I)"] * 5 +
    ["👁️ 인식 방식 (S/N)"] * 5 +
    ["🧠 판단 방식 (T/F)"] * 5 +
    ["📅 생활 방식 (J/P)"] * 5
)

scale_map = {
    "1": "① 전혀 아니다",
    "2": "② 아닌 편이다",
    "3": "③ 보통이다",
    "4": "④ 그런 편이다",
    "5": "⑤ 매우 그렇다",
}

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza..."
    )
    st.caption("키는 저장되지 않습니다")
    st.markdown("---")
    st.markdown("**점수 기준**")
    st.markdown("① 전혀 아니다")
    st.markdown("② 아닌 편이다")
    st.markdown("③ 보통이다")
    st.markdown("④ 그런 편이다")
    st.markdown("⑤ 매우 그렇다")

# 질문 폼
answers = []
current_section = ""

with st.form("mbti_form"):
    for i, (q, sec) in enumerate(zip(questions, sections)):
        if sec != current_section:
            st.markdown("---")
            st.subheader(sec)
            current_section = sec

        ans = st.select_slider(
            f"Q{i+1}. {q}",
            options=["1", "2", "3", "4", "5"],
            format_func=lambda x: scale_map[x],
            value="3",
            key=f"q{i}"
        )
        answers.append(ans)

    st.markdown("---")
    submitted = st.form_submit_button(
        "🔍 나의 MBTI + 짝궁 분석하기",
        use_container_width=True
    )

# 실행
if submitted:
    if not api_key:
        st.error("사이드바에 Gemini API Key를 입력하세요")
        st.stop()

    answer_str = ",".join(answers)

    # 간단 미리보기
    st.info(f"입력된 답변: {answer_str}")

    with st.spinner("🤖 AI 분석 중... (1~2분 소요)"):
        try:
            result = run_mbti_crew(answer_str, api_key)
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(result)

        except Exception as e:
            st.error(f"오류 발생: {e}")
            st.info("API Key를 확인하거나 다시 시도해주세요")