# app.py
import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="음식 맞추기 게임", layout="centered")

# ---------------------------
# 음식 데이터셋
# (이름, 카테고리, 이모지, 힌트 리스트)
# ---------------------------
foods = [
    # 한식
    ("김치찌개", "한식", "🍲", ["한국인들의 집밥 단골 메뉴", "밥도둑이라고 불린다"]),
    ("비빔밥", "한식", "🥘", ["여러 가지 재료가 어우러진다", "돌솥에 담기기도 한다"]),
    ("불고기", "한식", "🍖", ["간장 양념으로 조리한다", "달콤짭짤하다"]),
    ("삼겹살", "한식", "🥓", ["직접 구워 먹는 음식", "쌈과 함께 자주 먹는다"]),
    ("떡볶이", "한식", "🌶️", ["빨갛고 매운 소스", "길거리 음식으로 유명하다"]),
    ("갈비탕", "한식", "🍖", ["소고기 뼈로 끓인다", "국물이 맑다"]),
    ("잡채", "한식", "🍜", ["당면이 주재료", "잔치 음식으로 자주 등장한다"]),
    ("순두부찌개", "한식", "🥣", ["부드러운 두부가 주재료", "맵게 끓인다"]),

    # 일식
    ("초밥", "일식", "🍣", ["작은 한 입 요리", "간장과 함께 곁들인다"]),
    ("라멘", "일식", "🍜", ["뜨거운 국물 면 요리", "다양한 육수 맛"]),
    ("우동", "일식", "🥢", ["면발이 굵다", "일본 전통 국물 요리"]),
    ("돈카츠", "일식", "🍱", ["바삭한 튀김 옷", "특제 소스와 함께 먹는다"]),
    ("타코야끼", "일식", "🐙", ["밀가루 반죽 안에 문어가 들어간다", "둥근 모양 간식"]),
    ("규동", "일식", "🥩", ["양파와 고기를 간장 양념으로 조림", "밥 위에 얹어 먹는다"]),

    # 양식
    ("피자", "양식", "🍕", ["이탈리아에서 시작된 음식", "조각으로 잘라 먹는다"]),
    ("햄버거", "양식", "🍔", ["빵 사이에 고기 패티가 들어간다", "패스트푸드 대표 음식"]),
    ("스테이크", "양식", "🥩", ["고기를 두껍게 구워낸다", "레스토랑의 대표 메뉴"]),
    ("파스타", "양식", "🍝", ["면 요리", "토마토, 크림 등 다양한 소스"]),
    ("샐러드", "양식", "🥗", ["채소 위주 음식", "다이어트 식단에 자주 등장"]),
    ("핫도그", "양식", "🌭", ["빵 안에 소시지가 들어간다", "케첩과 머스터드 소스"]),

    # 간식 / 디저트
    ("도넛", "간식", "🍩", ["튀긴 밀가루 반죽", "달콤하고 동그랗다"]),
    ("케이크", "간식", "🍰", ["생일에 자주 먹는다", "크림과 장식"]),
    ("아이스크림", "간식", "🍦", ["차가운 디저트", "여름에 인기 많다"]),
    ("마카롱", "간식", "🍬", ["프랑스 디저트", "알록달록한 색깔"]),
    ("초콜릿", "간식", "🍫", ["달콤하다", "발렌타인데이에 주고받는다"]),
    ("붕어빵", "간식", "🐟", ["겨울 길거리 음식", "팥소가 들어간다"])
]

# ---------------------------
# 초기화
# ---------------------------
if "secret_food" not in st.session_state:
    st.session_state.secret_food, st.session_state.category, st.session_state.emoji, st.session_state.hints = random.choice(foods)
if "tries" not in st.session_state:
    st.session_state.tries = 0
if "finished" not in st.session_state:
    st.session_state.finished = False
if "hint_index" not in st.session_state:
    st.session_state.hint_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# ---------------------------
# UI
# ---------------------------
st.title("🍴 음식 맞추기 게임")
st.write("랜덤으로 선택된 음식을 맞춰보세요! 🎯")

# 난이도 선택
difficulty = st.radio("난이도 선택", ["쉬움", "보통", "어려움"], index=1)

# 카테고리와 이모지 힌트
st.info(f"카테고리: **{st.session_state.category}**")

# 정답 입력
guess = st.text_input("정답은 무엇일까요?").strip()

# ---------------------------
# 추측 버튼
# ---------------------------
if st.button("추측하기"):
    if not st.session_state.finished:
        st.session_state.tries += 1
        if guess == st.session_state.secret_food:
            # 점수 계산
            if st.session_state.hint_index == 0:
                gained = 10
            elif st.session_state.hint_index == 1:
                gained = 7
            else:
                gained = 5
            st.session_state.score += gained

            st.success(f"🎉 정답입니다! 정답은 {st.session_state.secret_food} 였어요.")
            st.info(f"총 {st.session_state.tries}번 만에 맞췄습니다!")
            st.success(f"획득 점수: {gained}점, 총 점수: {st.session_state.score}점")

            # 리더보드 기록
            st.session_state.leaderboard.append({
                "player": "나",
                "food": st.session_state.secret_food,
                "tries": st.session_state.tries,
                "score": st.session_state.score
            })

            st.session_state.finished = True
        else:
            st.warning("❌ 틀렸습니다! 다시 시도해보세요.")

# ---------------------------
# 힌트 버튼
# ---------------------------
max_hints = {"쉬움": 10, "보통": 2, "어려움": 0}[difficulty]
if st.session_state.hint_index < min(len(st.session_state.hints), max_hints) and not st.session_state.finished:
    if st.button("💡 힌트 보기"):
        st.write(f"👉 힌트 {st.session_state.hint_index+1}: {st.session_state.hints[st.session_state.hint_index]}")
        st.session_state.hint_index += 1

# ---------------------------
# 실패 처리
# ---------------------------
if not st.session_state.finished and st.session_state.tries >= 5:
    st.error(f"😢 기회를 모두 소진했습니다. 정답은 **{st.session_state.secret_food}** 였어요.")
    st.session_state.finished = True

# ---------------------------
# 다시 시작 버튼
# ---------------------------
if st.button("🔄 다시 시작"):
    st.session_state.secret_food, st.session_state.category, st.session_state.emoji, st.session_state.hints = random.choice(foods)
    st.session_state.tries = 0
    st.session_state.finished = False
    st.session_state.hint_index = 0
    st.experimental_rerun()

# ---------------------------
# 리더보드 표시
# ---------------------------
if len(st.session_state.leaderboard) > 0:
    st.subheader("🏆 나의 점수 기록")
    df = pd.DataFrame(st.session_state.leaderboard)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 점수 기록 다운로드 (CSV)", csv, "leaderboard.csv", "text/csv")
