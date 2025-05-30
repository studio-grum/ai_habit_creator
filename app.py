import streamlit as st
import google.generativeai as genai

# Gemini API 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Gemini 모델 초기화
model = genai.GenerativeModel('gemini-1.5-flash')

# 페이지 설정
st.set_page_config(
    page_title="나와 맞는 습관 찾기",
    page_icon="✨",
    layout="centered"
)

# 페이지 제목
st.title("나와 맞는 습관 찾기")

# MBTI 선택 드롭다운
mbti_options = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "당신의 MBTI를 선택해주세요",
    options=mbti_options,
    index=None,
    placeholder="MBTI를 선택하세요"
)

# 목표 분야 입력
goal_area = st.text_input(
    "목표로 하는 분야를 입력해주세요",
    placeholder="예: 자기계발, 건강관리, 생활습관 등"
)

# 추천 버튼
if st.button("나에게 맞는 습관 추천받기", type="primary"):
    if not selected_mbti:
        st.warning("MBTI를 선택해주세요!")
    elif not goal_area:
        st.warning("목표 분야를 입력해주세요!")
    else:
        try:
            # 로딩 표시
            with st.spinner("AI가 당신에게 맞는 습관을 찾고 있어요... 🤔"):
                # 프롬프트 구성
                prompt = f"""
                당신은 MBTI 전문가이자 습관 형성 전문가입니다. 
                다음 정보를 바탕으로 사용자에게 맞는 습관을 추천해주세요:

                - MBTI: {selected_mbti}
                - 목표 분야: {goal_area}

                다음 형식으로 3가지 습관을 추천해주세요:

                1. [습관 이름]
                   - 설명: [이 MBTI에게 왜 이 습관이 잘 맞는지 설명]
                   - 실행 팁: [이 습관을 쉽게 시작할 수 있는 구체적인 팁]

                2. [습관 이름]
                   - 설명: [이 MBTI에게 왜 이 습관이 잘 맞는지 설명]
                   - 실행 팁: [이 습관을 쉽게 시작할 수 있는 구체적인 팁]

                3. [습관 이름]
                   - 설명: [이 MBTI에게 왜 이 습관이 잘 맞는지 설명]
                   - 실행 팁: [이 습관을 쉽게 시작할 수 있는 구체적인 팁]

                반드시 한국어로 답변해주세요.
                """

                # Gemini API 호출
                response = model.generate_content(prompt)
                
                # 결과 표시
                st.markdown("### 🎯 당신에게 맞는 습관 추천")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
