# agents.py
from crewai import Agent, Task, Crew, LLM
from tools import mbti_test, mbti_chemistry

def run_mbti_crew(answer_str: str, api_key: str) -> str:
    my_llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=api_key,
        temperature=0.7
    )

    tester = Agent(
        role="MBTI 성격 진단 전문가",
        goal="20개 질문 답변으로 정확한 MBTI를 진단한다",
        backstory=(
            "당신은 15년 경력의 심리 상담사입니다. "
            "반드시 mbti_test 도구를 사용해서 진단하세요. "
            "경계형 MBTI가 나오면 두 가지 가능성을 함께 설명해주세요. "
            "결과는 따뜻하고 이해하기 쉽게 설명합니다. "
            "반드시 한국어로 답변하세요."
        ),
        tools=[mbti_test],
        llm=my_llm,
        verbose=True
    )

    matcher = Agent(
        role="MBTI 궁합 분석 전문가",
        goal="진단된 MBTI를 바탕으로 최적의 짝궁 유형을 관계별로 분석한다",
        backstory=(
            "당신은 MBTI 기반 인간관계 전문 컨설턴트입니다. "
            "반드시 mbti_chemistry 도구를 사용하세요. "
            "연인/친구/직장 각각 TOP 3 짝궁을 분석해주세요. "
            "결과는 긍정적이고 따뜻한 톤으로 작성합니다. "
            "반드시 한국어로 답변하세요."
        ),
        tools=[mbti_chemistry],
        llm=my_llm,
        verbose=True
    )

    reporter = Agent(
        role="성격 분석 리포트 작성가",
        goal="MBTI 진단과 궁합 분석 결과를 완성된 리포트로 작성한다",
        backstory=(
            "당신은 심리 분석 보고서 전문 작가입니다. "
            "아래 구조로 반드시 작성하세요:\n"
            "1. 나의 MBTI와 성격 특징\n"
            "2. 나의 강점과 약점\n"
            "3. 최적 짝궁 TOP 3 (연인/친구/직장)\n"
            "4. 짝궁별 관계 조언\n"
            "5. 오늘의 한마디\n"
            "친근하고 재미있는 톤을 유지하세요. "
            "반드시 한국어로 답변하세요."
        ),
        llm=my_llm,
        verbose=True
    )

    task1 = Task(
        description=(
            f"아래 20개 답변(1~5점)으로 MBTI를 진단하세요.\n"
            f"답변: {answer_str}\n"
            f"mbti_test 도구를 반드시 사용하세요.\n"
            f"경계형이 있으면 함께 설명해주세요."
        ),
        expected_output="MBTI 유형 + 각 지표별 성향 강도 + 경계형 여부",
        agent=tester
    )

    task2 = Task(
        description=(
            "진단된 MBTI를 바탕으로 짝궁을 분석하세요.\n"
            "mbti_chemistry 도구로 아래를 분석하세요:\n"
            "- 연인 궁합 TOP 3\n"
            "- 친구 궁합 TOP 3\n"
            "- 직장 궁합 TOP 3\n"
            "각각 도구를 호출해서 결과를 가져오세요."
        ),
        expected_output="관계별 최적 궁합 MBTI TOP 3와 이유",
        agent=matcher
    )

    task3 = Task(
        description=(
            "앞선 진단과 궁합 분석을 바탕으로 완성된 리포트를 작성하세요.\n"
            "재미있고 따뜻한 톤으로, 읽는 사람이 자신을 더 잘 이해할 수 있게 작성하세요.\n"
            "이모지를 적절히 사용해서 읽기 쉽게 만들어주세요."
        ),
        expected_output="완성된 MBTI 성격 + 짝궁 분석 리포트",
        agent=reporter
    )

    crew = Crew(
        agents=[tester, matcher, reporter],
        tasks=[task1, task2, task3],
        verbose=True
    )

    return str(crew.kickoff())