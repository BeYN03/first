# app.py
import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="음식 맞추기 게임", layout="centered")

# ---------------------------
# 음식 데이터셋
# ---------------------------
foods = [
    ("김치찌개", "한식", "🍲", ["한국인들의 집밥 단골 메뉴", "밥도둑이라고 불린다"]),
    ("비빔밥", "한식", "🥘", ["여러 가지 재료가 어우러진다", "돌솥에 담기기도 한다"]),
    ("불고기", "한식", "🍖", ["간장 양념으로 조리한다", "달콤짭짤하다"]),
    ("삼겹살", "한식", "🥓", ["직접 구워 먹는 음식", "쌈과 함께 자주 먹는다"]),
    ("떡볶이", "한식", "🌶️", ["빨갛고 매운 소스", "길거리 음식으로 유명하다"]),
    ("초밥", "일식", "🍣", ["작은 한 입 요리", "간장과 함께 곁들인다"]),
    ("라멘", "일식", "🍜", ["뜨거운 국물 면 요리", "다양한 육수 맛"]),
    ("피자", "양식", "🍕", ["이탈리아에서 시작된 음식", "조각으로 잘라 먹는다"]),
    ("햄버거", "양식", "🍔", ["빵 사이에 고기 패티가 들어간다", "패스트푸드 대표 음식"]),
    ("아이스크림", "간식", "🍦", ["차가운 디저트", "여름에 인기 많다"]),
    ("붕어빵", "간식", "🐟", ["겨울 길거리 음식", "팥소가 들어간다"])
]

# ---------------------------
# 게임 초기화 함수
# ---------------------------
def init_game():
    food = random.choice(foods)
    st.session_state.secret_food = food[0]
    st.session_state.category = food[1]
    st.session_state.emoji = food[2]
    st.session_state.hints = food[3]
    st.session_state.tries = 0
    st.session_state.finished = False
    st.session_state.hint_index = 0

if "secret_food" not in st.session_state:
    init_game()

if "score" not in st.session_state:
    st.session_state.score = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# ---------------------------
# UI
# ---------------------------
st.title("🍴 음식 맞추기 게임 (오류 수정 버전)")

difficulty = st.radio("난이도 선택", ["쉬움", "보통", "어려움"], index=1)

st.info(f"카테고리: **{st.session_state.category}**")

guess = st.text_input("정답은 무엇일까요? (예: 피자, 김치찌개)").strip()

# ---------------------------
# 추측
# ---------------------------
if st.button("추측하기"):
    if not st.session_state.finished:
        st.session_state.tries += 1
        if guess == st.session_state.secret_food:
            if st.session_state.hint_index == 0:
                gained = 10
            elif st.session_state.hint_index == 1:
                gained = 7
            else:
                gained = 5
            st.session_state.score += gained

            st.success(f"🎉 정답입니다! {st.session_state.secret_food}")
            st.info(f"{st.session_state.tries}번 만에 맞춤 ✅")
            st.success(f"+{gained}점 | 총 점수: {st.session_state.score}점")

            st.session_state.leaderboard.append({
                "food": st.session_state.secret_food,
                "tries": st.session_state.tries,
                "score": st.session_state.score
            })
            st.session_state.finished = True
        else:
            st.warning("❌ 틀렸습니다!")

# ---------------------------
# 힌트
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
    st.error(f"😢 5번 틀림 → 정답은 {st.session_state.secret_food} 였어요!")
    st.session_state.finished = True

# ---------------------------
# 다시 시작
# ---------------------------
if st.button("🔄 다시 시작"):
    init_game()

# ---------------------------
# 리더보드
# ---------------------------
if len(st.session_state.leaderboard) > 0:
    st.subheader("🏆 점수 기록")
    df = pd.DataFrame(st.session_state.leaderboard)
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 CSV 다운로드", df.to_csv(index=False), "leaderboard.csv")
