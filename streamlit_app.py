import streamlit as st
import datetime
import calendar
import json
import os
import matplotlib.pyplot as plt

# ------------------- 기본 설정 -------------------
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(KST).date()
st.set_page_config(page_title="카페인 관리 앱", layout="centered")

# ------------------- 데이터 불러오기 -------------------
DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        st.session_state.data = json.load(f)
else:
    st.session_state.data = {}

# ------------------- 상태 초기화 -------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "intake_input" not in st.session_state:
    st.session_state.intake_input = 0
if "selected_products" not in st.session_state:
    st.session_state.selected_products = []
if "selected_article" not in st.session_state:
    st.session_state.selected_article = None

# ------------------- 아카이브 글 데이터 -------------------
archive_articles = {
    "카페인의 인체 작용과 부작용, 그리고 개인차와 청소년 주의사항": """
### 카페인의 인체 작용과 부작용

요즘은 하루 한두 잔의 커피가 일상이 되었지만,  
커피를 자주 찾게 되는 이유는 단순한 습관이 아니다.  
그 중심에는 ‘카페인’이라는 성분이 있다.  

카페인은 중추에 작용해 몸을 깨우고 집중력을 높이는 효과가 있으며,  
진통제나 감기약에도 포함되어 두통 완화에 도움을 주기도 한다.  
하지만 과하게 섭취하면 건강에 좋지 않은 영향을 줄 수 있다.  

그렇다면 카페인은 어떤 원리로 우리 몸에 작용할까?  
카페인은 신체의 에너지 대사를 촉진하는 코르티솔 호르몬 분비를 증가시킨다.  
또한 뇌에서 흥분을 억제하는 채널의 활성화를 막아  
신경세포가 더 활발하게 반응하도록 만든다.  
이로 인해 일시적으로 기분이 좋아지고,  
행복감과 활력이 느껴지는 각성 효과가 나타난다.  

그러나 카페인을 과다하게 섭취하면  
불면, 심장이 빠르게 뛰는 심계항진, 혈압 상승, 손의 떨림,  
불안감 같은 부작용이 생길 수 있다.  

카페인은 글루타민과 도파민의 분비도 함께 증가시키는데,  
카페인의 각성작용과 집중력 증가는 이 같은 ‘흥분 효과’로 나타나게 된다.  
특히 카페인 대사가 느린 사람은  
카페인이 섭취량이 늘어나면 심장 질환이나 고혈압, 신장 질환의 위험이 커진다고 알려져 있다.  
반대로 대사가 빠른 사람은 같은 양을 마셔도 각성 효과가 빨리 사라진다.  

---

### 카페인과 수면의 관계

커피를 마시면 잠이 오지 않는 이유는 바로 아데노신 수용체 때문이다.  
우리 몸은 깨어 있을 때 아데노신이라는 물질을 점점 축적하는데,  
이 아데노신이 수용체에 결합하면 피로를 느끼고 잠이 온다.  

그런데 아데노신 수용체는 카페인과 아데노신을 구분하지 못한다.  
카페인을 섭취하면 수용체가 아데노신 대신 카페인을 받아들이게 된다.  
결국 수면 작용 대신 각성작용이 발생한다.  

이때 몸속의 카페인이 분해되기 전에는  
몸이 다시 자연스럽게 잠들기 어렵다.  
그래서 자기 전 커피를 마시면  
총 수면 시간이 줄어들거나, 수면의 질이 나빠지게 된다.  

다만 이 효과의 강도는 사람마다 다르다.  
카페인을 빨리 분해하는 유전자를 가진 사람은 반감기가 짧아  
각성 효과가 금방 사라지지만,  
대사가 느리거나 아데노신 수용체가 적은 사람은  
커피 한 잔만으로도 오랫동안 잠들기 힘들다.  

또 커피를 마신 뒤 잠이 잘 온다는 사람도  
카페인양이 많거나 잠들기 얼마 전에 커피를 마시면  
일부 아데노신 수용체가 카페인과 결합한 상태가 되고,  
깊은 잠이 줄고 얕은 잠이 증가해  
자각하지 못하는 상태로 수면의 질이 떨어질 수 있다.  

---

### 청소년은 특히 주의해야 해요

카페인은 흥분·중독성 약물이다.  
카페인 복용 후 지나친 도파민 분비로 인한 중독 가능성은  
뇌의 민감도가 높은 어린 나이일수록 더욱 강해질 수 있다.  

또한 카페인은 성장기 뇌 세포 발달에도 영향을 미칠 수 있으므로,  
청소년은 가능하면 에너지음료나 고카페인 음료 섭취를 줄이는 것이 좋다.
""",

    "커피의 카페인 함량이 일정하지 않다고?": """
그는 또 한 가지 흥미로운 점을 지적했다.  
커피의 카페인 농도는 낮아졌지만, 커피잔의 크기는 오히려 커졌다는 것이다.  
요즘 판매되는 ‘작은 사이즈’ 커피조차 295ml 정도이며,  
스타벅스의 그란데 사이즈(472ml) 한 잔에는  
던킨도너츠 커피의 두 배에 가까운 카페인이 들어 있었다.

심지어 같은 매장에서 같은 메뉴를 주문해도 함량이 일정하지 않았다.  
골드버거는 6일 연속 같은 블렌드 커피를 구입했는데,  
카페인 양은 하루는 260mg, 또 다른 날은 564mg으로 두 배 이상 차이가 났다.

이후 스코틀랜드의 토머스 크로지어(2012) 연구팀도  
비슷한 결과를 발표했다.  
그들은 글래스고 지역의 여러 카페에서 구입한 에스프레소 20잔을 분석했는데,  
각 잔의 용량은 23.6~70.8ml로 다르지만,  
부피 차이를 고려하더라도 카페인 농도는 매우 불규칙했다.  
실제 측정 결과, 에스프레소 한 잔에 들어 있는 카페인은 51mg에서 300mg 이상까지 달랐고,  
이를 29.5ml 기준으로 환산한 농도는 56~196mg으로 나타났다.  
즉, 같은 용량으로 환산해도 최대 3배 이상 차이난 것이다.  
심지어 스타벅스 에스프레소는 가장 낮은 51mg 수준이었고,  
다른 카페에서는 300mg을 훌쩍 넘는 경우도 있었다.

이 연구들은 중요한 사실을 알려준다.  
커피 한 잔 속 카페인 함량은 결코 일정하지 않다.  
원두의 품종, 재배 환경, 로스팅 정도, 추출 시간,  
그리고 물과 커피가루의 비율에 따라 카페인 양이 크게 달라진다.

그래서 함량이 낮은 커피는 임산부나 카페인 제한이 필요한 사람도  
하루 네 잔 정도는 비교적 안전하게 마실 수 있다.  
하지만 카페인이 많은 커피라면 에스프레소 한 잔만으로도  
하루 권장량인 200mg을 훌쩍 넘길 수 있다.

결국, 우리가 매일 마시는 커피는 ‘하루의 기분’을 바꿀 만큼  
카페인 양의 차이가 크다.  
같은 카페, 같은 메뉴라도 어떤 날엔 안정적이고 집중이 잘 되지만,  
다른 날엔 심장이 빨리 뛰거나 불안해지는 이유—  
그건 바로 커피마다, 심지어 같은 커피 안에서도  
카페인 함량이 제각각이기 때문이다.
"""
}

# ------------------- 홈 화면 -------------------
if st.session_state.page == "home":
    st.title("☕ 카페인 관리 앱")
    st.write("기능을 선택하세요.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📅 카페인 달력", use_container_width=True):
            st.session_state.page = "calendar"
    with col2:
        if st.button("📚 카페인 아카이브", use_container_width=True):
            st.session_state.page = "archive"
    with col3:
        if st.button("⏰ 섭취 시간대별 영향", use_container_width=True):
            st.session_state.page = "timing"
    with col4:
        if st.button("🧠 카페인 자가진단", use_container_width=True):
            st.session_state.page = "survey"

# ------------------- 카페인 달력 -------------------
elif st.session_state.page == "calendar":
    st.title("📅 카페인 달력")
    st.write("목표 섭취량을 설정하고 달성 여부를 기록하세요.")

    year = today.year
    month = st.selectbox("월 선택", range(1, 13), index=today.month - 1, format_func=lambda x: f"{x}월")
    month_days = calendar.monthrange(year, month)[1]
    cols = st.columns(7)

    for i, day in enumerate(range(1, month_days + 1)):
        col = cols[i % 7]
        with col:
            key = f"{year}-{month:02d}-{day:02d}"
            entry = st.session_state.data.get(key)
            label = f"{day}일"
            if entry:
                label += f"\n{entry['intake']}mg {'✅' if entry['achieved'] else '❌'}"
            if st.button(label, key=f"btn_{key}"):
                st.session_state.selected_date = key
                st.session_state.intake_input = 0
                st.session_state.selected_products = []

    if "selected_date" in st.session_state:
        date = st.session_state.selected_date
        st.markdown("---")
        st.subheader(f"{date} 기록")

        goal = st.number_input("목표 섭취량 (mg)", min_value=0, step=10, key="goal_input")
        products = {
            "몬스터 에너지 355ml": 100,
            "레드불 에너지 드링크 355ml": 88.75,
            "핫식스 더킹 파워 355ml": 100,
            "핫식스 더킹 제로 355ml": 100
        }

        selected_product = st.selectbox("제품 선택", ["선택 안 함"] + list(products.keys()), key="product_select")
        if selected_product != "선택 안 함":
            if st.button("선택한 제품 추가"):
                caffeine_value = products[selected_product]
                st.session_state.selected_products.append((selected_product, caffeine_value))
                st.session_state.intake_input += caffeine_value
                st.success(f"{selected_product} 추가됨 (+{caffeine_value}mg)")

        st.markdown("---")
        st.write("직접 mg 단위로 추가하기")
        manual_value = st.number_input("직접 입력 (mg)", min_value=0, step=10, key="manual_add_value")
        if st.button("직접 추가"):
            if manual_value > 0:
                st.session_state.selected_products.append((f"수동 입력 {manual_value}mg", manual_value))
                st.session_state.intake_input += manual_value
                st.success(f"수동 입력으로 +{manual_value}mg 추가됨")

        if st.session_state.selected_products:
            st.write("### 오늘 추가한 항목")
            for name, mg in st.session_state.selected_products:
                st.write(f"- {name}: {mg}mg")
            st.metric(label="총 섭취량", value=f"{st.session_state.intake_input} mg")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("저장"):
                achieved = st.session_state.intake_input <= goal
                st.session_state.data[date] = {
                    "goal": goal,
                    "intake": st.session_state.intake_input,
                    "achieved": achieved,
                    "products": st.session_state.selected_products.copy()
                }
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.data, f, ensure_ascii=False, indent=2)
                del st.session_state.selected_date
                st.success(f"{date} 기록이 저장되었습니다!")
        with col2:
            if st.button("취소"):
                del st.session_state.selected_date
        with col3:
            if st.button("🏠 홈으로"):
                st.session_state.page = "home"
                if "selected_date" in st.session_state:
                    del st.session_state.selected_date

    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.page = "home"

# ------------------- 카페인 아카이브 -------------------
elif st.session_state.page == "archive":
    st.title("📚 카페인 아카이브")
    if st.session_state.selected_article is None:
        st.write("카페인 관련 정보를 선택하세요:")
        for title in archive_articles.keys():
            if st.button(title, use_container_width=True):
                st.session_state.selected_article = title
                st.rerun()

        st.markdown("---")
        if st.button("🏠 홈으로 돌아가기", use_container_width=True):
            st.session_state.page = "home"
    else:
        title = st.session_state.selected_article
        st.header(title)
        st.markdown(archive_articles[title])
        st.markdown("---")
        if st.button("⬅ 목록으로 돌아가기"):
            st.session_state.selected_article = None
            st.rerun()

# ------------------- 섭취 시간대별 영향 -------------------
elif st.session_state.page == "timing":
    st.title("⏰ 카페인 섭취 시간대별 수면 영향 (400mg 기준)")
    st.write("""
취침 예정 시간과 카페인 섭취 시간을 입력하면, 수면에 미치는 영향을 시각적으로 보여줍니다.  
본 시각화는 **400mg** 섭취 기준이며,  
연구에 따르면 **100mg은 취침 전 4시간까지 섭취해도 수면에 큰 영향을 미치지 않습니다.**
""")
    st.markdown("---")

    sleep_time = st.time_input("🛏️ 취침 예정 시간", datetime.time(23, 0))
    intake_time = st.time_input("☕ 카페인 섭취 시간", datetime.time(15, 0))

    sleep_dt = datetime.datetime.combine(datetime.date.today(), sleep_time)
    intake_dt = datetime.datetime.combine(datetime.date.today(), intake_time)
    if intake_dt > sleep_dt:
        intake_dt -= datetime.timedelta(days=1)
    hours_until_sleep = (sleep_dt - intake_dt).total_seconds() / 3600

    if hours_until_sleep >= 8:
        risk_level = "🟩 안전 (Safe)"
        advice = "카페인 대사가 충분히 이루어져 수면에 거의 영향을 주지 않습니다."
    elif 4 <= hours_until_sleep < 8:
        risk_level = "🟨 주의 (Moderate)"
        advice = "수면 효율이 약간 저하될 수 있습니다. 가능하면 취침 8시간 이전 섭취를 권장합니다."
    else:
        risk_level = "🟥 위험 (High Impact)"
        advice = "카페인이 체내에 상당량 남아 수면 시작이 지연되고 깊은 수면이 감소할 수 있습니다."

    st.subheader("결과 요약")
    st.write(f"☕ 섭취 시점: 취침 {hours_until_sleep:.1f}시간 전")
    st.write(f"📊 현재 구간: {risk_level}")
    st.info(advice)

    fig, ax = plt.subplots(figsize=(8, 1.5))
    zones = [
        (0, 4, "red"),
        (4, 8, "gold"),
        (8, 12, "green")
    ]
    for start, end, color in zones:
        ax.barh(0, width=end - start, left=start, color=color, alpha=0.5)
    ax.scatter(hours_until_sleep, 0, color="black", s=100, zorder=5)
    ax.set_xlim(0, 12)
    ax.set_yticks([])
    ax.set_xlabel("취침 전 남은 시간 (시간 단위)")
    ax.invert_xaxis()
    st.pyplot(fig)

    st.markdown("""
#### 그래프 해석 가이드
- **녹색 구간 (8~12시간 전)**: 카페인 대사가 충분히 이루어져 수면에 영향이 거의 없음  
- **노란색 구간 (4~8시간 전)**: 수면 효율이 약간 저하될 수 있음  
- **빨간색 구간 (0~4시간 전)**: 수면 시작이 지연되고 깊은 수면이 줄어듦  
- 검은 점은 사용자의 실제 **카페인 섭취 시점**을 나타냅니다.
""")

    st.caption("""
※ 근거: 400mg(고용량) 섭취 기준 — 취침 전 12시간 이내 섭취 시 수면 질 저하  
100mg은 취침 전 4시간까지 섭취해도 수면에 유의미한 영향이 없음  
(출처: Dose and timing effects of caffeine on subsequent sleep: a randomized clinical crossover trial, 2024)
""")

    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.page = "home"

# ------------------- 카페인 자가진단 -------------------
elif st.session_state.page == "survey":
    st.title("🧠 카페인 자가진단")
    st.caption("이 검사는 전문 의료 지식을 바탕으로 제작된 진단이 아니며, 임시적인 자가 점검입니다. 참고 지표로만 활용하세요.")

    st.write("아래 문항은 최근 2~4주를 기준으로 체크하세요.")
    st.markdown("---")

    options = ["전혀 아니다", "가끔 그렇다", "자주 그렇다", "거의 항상 그렇다"]
    score_map = {"전혀 아니다": 0, "가끔 그렇다": 1, "자주 그렇다": 2, "거의 항상 그렇다": 3}

    questions = [
        "아침에 카페인을 섭취하지 않으면 하루를 시작하기 어렵다.",
        "예전보다 같은 효과를 느끼기 위해 카페인 섭취량이 늘었다.",
        "카페인을 마시지 않으면 두통, 피로, 무기력 같은 금단 느낌이 있다.",
        "카페인 섭취를 줄이려고 시도했지만 잘 안 됐다.",
        "피곤하지 않아도 습관적으로 카페인 음료를 찾는다.",
        "카페인을 섭취한 뒤 심장이 빨리 뛰거나 손이 떨린 적이 있다.",
        "카페인 섭취 때문에 잠드는 시간이 늦어지거나 수면의 질이 떨어진다.",
        "오후(또는 저녁)에도 카페인을 섭취하는 날이 많다.",
        "카페인을 마시지 않으면 예민해지거나 집중이 더 안 되는 느낌이 든다.",
        "카페인 때문에 속이 쓰리거나 메스꺼움 같은 불편을 느낀 적이 있다.",
        "카페인 섭취량이 어느 정도인지 정확히 모른 채 마시는 편이다.",
        "카페인을 마셔도 피로가 충분히 회복되지 않아 더 찾게 된다.",
        "카페인 섭취 후 불안감/초조함이 심해진 적이 있다.",
        "카페인을 줄여야 한다고 생각하면서도 계속 섭취한다.",
        "하루 섭취량이 많아도(또는 늦게 마셔도) 스스로 통제하기 어렵다."
    ]

    total = 0
    for i, q in enumerate(questions, start=1):
        ans = st.radio(f"{i}. {q}", options, key=f"survey_q{i}")
        total += score_map[ans]

    st.markdown("---")
    st.subheader("점수")
    st.write(f"총점: {total} / 45")

    if total <= 9:
        st.success("중독(의존) 가능성 낮음: 현재는 생활 습관 수준일 가능성이 큽니다.")
    elif total <= 18:
        st.info("중독(의존) 가능성 보통: 섭취 시간(특히 오후)과 섭취량 점검이 필요합니다.")
    elif total <= 27:
        st.warning("중독(의존) 가능성 높음: 줄이기 계획을 세우고 섭취 기록을 권장합니다.")
    elif total <= 36:
        st.error("중독(의존) 가능성 매우 높음: 수면/불안/심박 관련 증상이 있으면 상담을 권장합니다.")
    else:
        st.error("중독(의존) 가능성 매우 높음(고위험): 스스로 줄이기 어렵다면 전문가 상담을 권장합니다.")

    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.page = "home"
