# tools.py
import random
from crewai.tools import tool

@tool("MBTI 진단")
def mbti_test(answers: str) -> str:
    '''20개 질문 답변으로 MBTI를 진단합니다.
    각 답변은 1~5 숫자로 입력하세요.
    1=전혀아니다, 2=아닌편이다, 3=보통이다, 4=그런편이다, 5=매우그렇다
    예: "4,2,3,5,4,2,3,1,4,2,5,3,2,4,1,5,4,3,2,4"
    반드시 20개를 쉼표로 구분해서 입력하세요.'''

    score_map = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}

    def get_strength(score, max_score=25):
        pct = score / max_score * 100
        if pct >= 80: return "매우 강함"
        if pct >= 65: return "강함"
        if pct >= 45: return "보통"
        if pct >= 30: return "약함"
        return "매우 약함"

    def is_border(score):
        pct = score / 25 * 100
        return 40 <= pct <= 60

    try:
        ans = [a.strip() for a in answers.split(",")]
        if len(ans) != 20:
            return f"20개 답변이 필요합니다. 현재 {len(ans)}개 입력됨"

        for i, a in enumerate(ans):
            if a not in score_map:
                return f"Q{i+1} 오류: '{a}' — 1~5 숫자만 입력 가능합니다"

        scores = [score_map[a] for a in ans]
        ei = sum(scores[0:5])
        sn = sum(scores[5:10])
        tf = sum(scores[10:15])
        jp = sum(scores[15:20])

        e_or_i = "E" if ei > 15 else "I"
        s_or_n = "S" if sn > 15 else "N"
        t_or_f = "T" if tf > 15 else "F"
        j_or_p = "J" if jp > 15 else "P"
        mbti = e_or_i + s_or_n + t_or_f + j_or_p

        borders = []
        if is_border(ei): borders.append("E/I")
        if is_border(sn): borders.append("S/N")
        if is_border(tf): borders.append("T/F")
        if is_border(jp): borders.append("J/P")

        border_msg = ""
        if borders:
            border_msg = f"\n⚠️ 경계형: {', '.join(borders)} — 상황에 따라 다르게 나타날 수 있어요"

        return (
            f"[MBTI 진단 결과]\n"
            f"당신의 MBTI: {mbti}\n\n"
            f"E/I: {e_or_i}({'외향' if e_or_i=='E' else '내향'}) "
            f"— {get_strength(ei if ei>15 else 26-ei)} (점수: {ei}/25)\n"
            f"S/N: {s_or_n}({'감각' if s_or_n=='S' else '직관'}) "
            f"— {get_strength(sn if sn>15 else 26-sn)} (점수: {sn}/25)\n"
            f"T/F: {t_or_f}({'사고' if t_or_f=='T' else '감정'}) "
            f"— {get_strength(tf if tf>15 else 26-tf)} (점수: {tf}/25)\n"
            f"J/P: {j_or_p}({'판단' if j_or_p=='J' else '인식'}) "
            f"— {get_strength(jp if jp>15 else 26-jp)} (점수: {jp}/25)"
            f"{border_msg}"
        )
    except Exception as e:
        return f"오류: {e}"


@tool("MBTI 궁합")
def mbti_chemistry(query: str) -> str:
    '''두 MBTI의 궁합을 관계 유형에 따라 분석합니다.
    형식: "MBTI1,MBTI2,관계유형"
    관계유형: 연인, 친구, 직장, 부모자녀
    예: "INFP,ENFJ,연인"'''

    names = {
        "INTJ": "용의주도한 전략가", "INTP": "논리적인 사색가",
        "ENTJ": "대담한 통솔자",    "ENTP": "뜨거운 논쟁가",
        "INFJ": "선의의 옹호자",    "INFP": "열정적인 중재자",
        "ENFJ": "정의로운 사회운동가","ENFP": "재기발랄한 활동가",
        "ISTJ": "청렴결백한 논리주의자","ISFJ": "용감한 수호자",
        "ESTJ": "엄격한 관리자",    "ESFJ": "사교적인 외교관",
        "ISTP": "만능 재주꾼",      "ISFP": "호기심 많은 예술가",
        "ESTP": "모험을 즐기는 사업가","ESFP": "자유로운 영혼의 연예인",
    }

    compatibility = {
        ("INFP","ENFJ"): {
            "연인": (95, "천생연분", "감성 교감 최고", "ENFJ가 너무 이끌면 지침"),
            "친구": (90, "감성 단짝", "밤새 이야기 가능", "조언보다 공감이 필요"),
            "직장": (85, "드림팀", "창의+리더십 조합", "피드백은 조용히"),
            "부모자녀": (88, "따뜻한 교감", "감성 소통 자연스러움", "속도 존중 필요"),
        },
        ("INTJ","ENTP"): {
            "연인": (82, "지적 라이벌", "함께 성장하는 커플", "냉전이 길어질 수 있음"),
            "친구": (88, "논쟁 단짝", "끝없는 토론이 즐거움", "감정도 챙겨야 함"),
            "직장": (92, "혁신 듀오", "전략+아이디어 무적", "역할 분담 명확히"),
            "부모자녀": (75, "까다로운 관계", "지적 호기심 공유", "칭찬을 더 해주세요"),
        },
        ("ENFP","INFJ"): {
            "연인": (92, "영혼의 단짝", "에너지가 내면을 깨움", "혼자만의 시간 배려"),
            "친구": (89, "이상적 우정", "서로의 꿈을 응원", "현실 감각도 필요"),
            "직장": (83, "비전 팀", "창의적 시너지", "마감 관리 주의"),
            "부모자녀": (86, "활기찬 관계", "자유로운 소통", "규칙도 함께 만들기"),
        },
        ("ISTJ","ENFP"): {
            "연인": (74, "정반대 매력", "안정감+활력 보완", "생활 방식 차이 조율 필요"),
            "친구": (78, "의외의 찰떡", "서로 없는 것을 채워줌", "페이스 맞추기 중요"),
            "직장": (80, "균형 팀", "실행력+아이디어 조합", "소통 방식 맞춰야 함"),
            "부모자녀": (72, "성장하는 관계", "서로에게 배울 점 많음", "강요보다 존중"),
        },
        ("ESFJ","ISFP"): {
            "연인": (83, "따뜻한 동반자", "서로 아끼고 배려", "ESFJ가 과하게 챙기면 부담"),
            "친구": (85, "다정한 친구", "편안하고 따뜻한 관계", "ISFP 혼자만의 시간 존중"),
            "직장": (79, "조화로운 팀", "분위기 메이커 조합", "갈등 회피 경향 주의"),
            "부모자녀": (84, "다정한 관계", "정서적 지지 강함", "자율성도 허용해주세요"),
        },
    }

    relation_templates = {
        "연인": ("연애 궁합", "설레는 점", "주의할 점"),
        "친구": ("우정 궁합", "잘 맞는 점", "싸울 수 있는 점"),
        "직장": ("업무 궁합", "시너지", "갈등 주의"),
        "부모자녀": ("부모자녀 궁합", "잘 통하는 점", "세대차이 주의"),
    }

    try:
        parts = [p.strip() for p in query.split(",")]
        if len(parts) == 3:
            a, b, relation = parts[0].upper(), parts[1].upper(), parts[2]
        elif len(parts) == 2:
            a, b, relation = parts[0].upper(), parts[1].upper(), "연인"
        else:
            return '"INFP,ENFJ,연인" 형식으로 입력하세요'

        if a not in names: return f'"{a}"는 올바른 MBTI가 아닙니다'
        if b not in names: return f'"{b}"는 올바른 MBTI가 아닙니다'
        if relation not in relation_templates:
            return '관계유형은 연인/친구/직장/부모자녀 중 하나를 입력하세요'

        label, strong_msg, caution_msg = relation_templates[relation]

        if a == b:
            return (
                f"[{a} × {b} {label}]\n"
                f"거울 커플! 서로를 너무 잘 알지만 단점도 2배\n"
                f"궁합: 78점 ★★★☆☆\n\n※ 재미로만 참고하세요!"
            )

        key = (a,b) if (a,b) in compatibility else \
              (b,a) if (b,a) in compatibility else None

        if key and relation in compatibility[key]:
            score, one_line, strength, caution = compatibility[key][relation]
            stars = "★" * (score // 20) + "☆" * (5 - score // 20)
            return (
                f"[{a} × {b} {label}]\n"
                f"{names[a]} × {names[b]}\n\n"
                f"궁합: {score}점 {stars}\n"
                f"한줄평: {one_line}\n\n"
                f"{strong_msg}: {strength}\n"
                f"{caution_msg}: {caution}\n\n"
                f"※ 재미로만 참고하세요!"
            )

        score = random.randint(68, 91)
        e_i = sum(1 for x in [a,b] if x[0]=='E')
        auto_tip = {
            2: "둘 다 외향형! 에너지 넘치는 조합",
            0: "둘 다 내향형! 깊은 교감의 조합",
            1: "외향-내향 밸런스 좋은 조합",
        }
        stars = "★" * (score // 20) + "☆" * (5 - score // 20)
        return (
            f"[{a} × {b} {label}]\n"
            f"{names[a]} × {names[b]}\n\n"
            f"궁합: {score}점 {stars}\n"
            f"팁: {auto_tip[e_i]}\n\n"
            f"※ 재미로만 참고하세요!"
        )

    except Exception as e:
        return f"오류: {e}"


if __name__ == "__main__":
    print(mbti_test.run("4,2,3,5,4,2,3,1,4,2,5,3,2,4,1,5,4,3,2,4"))
    print()
    print(mbti_chemistry.run("INFP,ENFJ,연인"))