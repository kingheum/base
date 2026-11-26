import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# KBO 2026 정규시즌 성적 기반 선수 영입 게임
# 게임 내 가치(억 원)는 실제 연봉이 아니라, 공개된 성적을
# 아래 공식에 대입해 계산한 게임용 가격입니다.
# ------------------------------------------------------------

SEASON = 2026

# 타자 데이터: 포지션별 OPS 상위 선수. OPS는 실제 2026 정규시즌 기록.
# 가격 공식: 3.0 + OPS * 5.0 (억 원)
BATTERS = [
    # 포수
    {"id": "han_junsu", "name": "한준수", "team": "KIA 타이거즈", "slot": "포수", "ops": 0.822, "avg": ".281", "hr": 7, "rbi": 38},
    {"id": "heo_inseo", "name": "허인서", "team": "한화 이글스", "slot": "포수", "ops": 0.821},
    {"id": "kang_minho", "name": "강민호", "team": "삼성 라이온즈", "slot": "포수", "ops": 0.798},
    # 1루수
    {"id": "austin_dean", "name": "오스틴 딘", "team": "LG 트윈스", "slot": "1루수", "ops": 1.062, "avg": ".331", "hr": 41, "rbi": 127},
    {"id": "castro", "name": "카스트로", "team": "KIA 타이거즈", "slot": "1루수", "ops": 0.928, "avg": ".327", "hr": 21, "rbi": 88},
    {"id": "davidson", "name": "데이비슨", "team": "키움 히어로즈", "slot": "1루수", "ops": 0.908},
    # 2루수
    {"id": "park_junsoon", "name": "박준순", "team": "두산 베어스", "slot": "2루수", "ops": 0.853, "avg": ".302", "hr": 16, "rbi": 61},
    {"id": "park_minwoo", "name": "박민우", "team": "NC 다이노스", "slot": "2루수", "ops": 0.839, "avg": ".320", "hr": 7, "rbi": 72},
    {"id": "ryu_hyunin", "name": "류현인", "team": "KT 위즈", "slot": "2루수", "ops": 0.817},
    # 3루수
    {"id": "kim_doyeong", "name": "김도영", "team": "KIA 타이거즈", "slot": "3루수", "ops": 1.060, "avg": ".308", "hr": 45, "rbi": 118},
    {"id": "choi_jeong", "name": "최정", "team": "SSG 랜더스", "slot": "3루수", "ops": 1.013, "avg": ".306", "hr": 20, "rbi": 57},
    {"id": "han_donghee", "name": "한동희", "team": "롯데 자이언츠", "slot": "3루수", "ops": 0.915, "avg": ".306", "hr": 25, "rbi": 81},
    # 유격수
    {"id": "park_seonghan", "name": "박성한", "team": "SSG 랜더스", "slot": "유격수", "ops": 0.854, "avg": ".330", "hr": 5, "rbi": 71},
    {"id": "lee_jaehyun", "name": "이재현", "team": "삼성 라이온즈", "slot": "유격수", "ops": 0.793},
    {"id": "kim_juwon", "name": "김주원", "team": "NC 다이노스", "slot": "유격수", "ops": 0.788},
    # 좌익수
    {"id": "koo_jawook", "name": "구자욱", "team": "삼성 라이온즈", "slot": "좌익수", "ops": 1.039, "avg": ".371", "hr": 15, "rbi": 102},
    {"id": "hilliard", "name": "샘 힐리어드", "team": "KT 위즈", "slot": "좌익수", "ops": 0.967, "avg": ".304", "hr": 44, "rbi": 139},
    {"id": "reyes", "name": "빅터 레이예스", "team": "롯데 자이언츠", "slot": "좌익수", "ops": 0.937, "avg": ".363", "hr": 18, "rbi": 109},
    # 중견수
    {"id": "choi_inho", "name": "최인호", "team": "한화 이글스", "slot": "중견수", "ops": 0.829, "avg": ".325", "hr": 5, "rbi": 24},
    {"id": "cheon_jaehwan", "name": "천재환", "team": "NC 다이노스", "slot": "중견수", "ops": 0.807},
    {"id": "kim_jichan", "name": "김지찬", "team": "삼성 라이온즈", "slot": "중견수", "ops": 0.756},
    # 우익수
    {"id": "ahn_hyunmin", "name": "안현민", "team": "KT 위즈", "slot": "우익수", "ops": 0.947, "avg": ".298", "hr": 14, "rbi": 63},
    {"id": "na_sungbum", "name": "나성범", "team": "KIA 타이거즈", "slot": "우익수", "ops": 0.920, "avg": ".303", "hr": 31, "rbi": 97},
    {"id": "choi_wonjun", "name": "최원준", "team": "KT 위즈", "slot": "우익수", "ops": 0.919, "avg": ".356", "hr": 9, "rbi": 74},
    # 지명타자
    {"id": "kang_baekho", "name": "강백호", "team": "한화 이글스", "slot": "지명타자", "ops": 0.883, "avg": ".285", "hr": 34, "rbi": 118},
    {"id": "park_geonwoo", "name": "박건우", "team": "NC 다이노스", "slot": "지명타자", "ops": 0.863, "avg": ".301", "hr": 20, "rbi": 78},
    {"id": "choi_hyungwoo", "name": "최형우", "team": "삼성 라이온즈", "slot": "지명타자", "ops": 0.849, "avg": ".301", "hr": 18, "rbi": 106},
]

# 선발투수: 가격 공식 = 2.0 + (5.0 - ERA)*0.9 + IP/250 + SO/250
STARTERS = [
    {"id": "gwak_been", "name": "곽빈", "team": "두산 베어스", "slot": "선발투수", "era": 2.24, "ip": 161.0, "so": 197, "w": 11},
    {"id": "adam_oller", "name": "애덤 올러", "team": "KIA 타이거즈", "slot": "선발투수", "era": 3.13, "ip": 178.0, "so": 180, "w": 11},
    {"id": "choi_minseok", "name": "최민석", "team": "두산 베어스", "slot": "선발투수", "era": 3.20, "ip": 146.33, "so": 129, "w": 14},
    {"id": "ko_youngpyo", "name": "고영표", "team": "KT 위즈", "slot": "선발투수", "era": 3.28, "ip": 172.67, "so": 183, "w": 15},
    {"id": "james_naile", "name": "제임스 네일", "team": "KIA 타이거즈", "slot": "선발투수", "era": 3.49, "ip": 183.0, "so": 156, "w": 13},
]

# 중간계투: 가격 공식 = 2.5 + 홀드 * 0.12
RELIEVERS = [
    {"id": "sugimoto", "name": "스기모토", "team": "KT 위즈", "slot": "중간계투", "holds": 25},
    {"id": "lee_seungmin", "name": "이승민", "team": "삼성 라이온즈", "slot": "중간계투", "holds": 23},
    {"id": "kim_min", "name": "김민", "team": "SSG 랜더스", "slot": "중간계투", "holds": 21},
    {"id": "kim_wonjung", "name": "김원중", "team": "롯데 자이언츠", "slot": "중간계투", "holds": 21},
    {"id": "cho_sangwoo", "name": "조상우", "team": "KIA 타이거즈", "slot": "중간계투", "holds": 21},
]

# 마무리투수: 가격 공식 = 3.0 + 세이브 * 0.10
CLOSERS = [
    {"id": "kim_jaeyoon", "name": "김재윤", "team": "삼성 라이온즈", "slot": "마무리투수", "saves": 35},
    {"id": "son_juyeong", "name": "손주영", "team": "LG 트윈스", "slot": "마무리투수", "saves": 31},
    {"id": "park_yeonghyun", "name": "박영현", "team": "KT 위즈", "slot": "마무리투수", "saves": 30},
    {"id": "lee_youngha", "name": "이영하", "team": "두산 베어스", "slot": "마무리투수", "saves": 26},
    {"id": "jo_byunghyeon", "name": "조병현", "team": "SSG 랜더스", "slot": "마무리투수", "saves": 24},
]

ALL_PLAYERS = BATTERS + STARTERS + RELIEVERS + CLOSERS
PLAYER_BY_ID = {p["id"]: p for p in ALL_PLAYERS}

SLOTS = [
    "포수", "1루수", "2루수", "3루수", "유격수", "좌익수", "중견수", "우익수", "지명타자",
    "선발투수 1", "선발투수 2", "선발투수 3", "중간계투 1", "중간계투 2", "마무리투수",
]

SOURCES = {
    "2026 KBO 공식 기록 - 타격": "https://eng.koreabaseball.com/Stats/battingleaders.aspx",
    "2026 KBO 공식 기록 - 투수": "https://eng.koreabaseball.com/stats/pitchingLeaders.aspx",
    "2026 포지션별 OPS 및 시즌 기록 정리": "https://yagulens.com/seasons/2026/rankings/",
    "2026 KBO 타자 OPS 통계": "https://mykbostats.com/stats/top/ops",
    "2026 KBO 투수 탈삼진 통계": "https://mykbostats.com/stats/top/k/2026",
}


def player_price(player: dict) -> float:
    """2026 실제 기록을 이용한 게임 내 가치(억 원). 실제 연봉이 아님."""
    if player["slot"] in {"포수", "1루수", "2루수", "3루수", "유격수", "좌익수", "중견수", "우익수", "지명타자"}:
        value = 3.0 + player["ops"] * 5.0
    elif player["slot"] == "선발투수":
        value = 2.0 + (5.0 - player["era"]) * 0.9 + player["ip"] / 250 + player["so"] / 250
    elif player["slot"] == "중간계투":
        value = 2.5 + player["holds"] * 0.12
    else:
        value = 3.0 + player["saves"] * 0.10
    return round(value, 1)


def player_rating(player: dict) -> float:
    """게임용 전력 점수(0~100 근사치)."""
    if "ops" in player:
        return min(100.0, player["ops"] * 100)
    if "era" in player:
        return max(55.0, min(100.0, 100 - player["era"] * 6 + player["so"] / 35))
    if "holds" in player:
        return min(100.0, 60 + player["holds"] * 1.3)
    return min(100.0, 60 + player["saves"] * 1.0)


def format_player_stats(player: dict) -> str:
    if "ops" in player:
        bits = [f"OPS {player['ops']:.3f}"]
        for key, label in [("avg", "타율"), ("hr", "홈런"), ("rbi", "타점")]:
            if key in player:
                bits.append(f"{label} {player[key]}")
        return " · ".join(bits)
    if "era" in player:
        return f"ERA {player['era']:.2f} · {player['ip']}이닝 · 탈삼진 {player['so']} · {player['w']}승"
    if "holds" in player:
        return f"홀드 {player['holds']}개"
    return f"세이브 {player['saves']}개"


def get_available_players(slot: str, roster: dict) -> list[dict]:
    """현재 슬롯에서 영입할 수 있고 이미 다른 슬롯에 없는 선수만 반환."""
    if slot in {"선발투수 1", "선발투수 2", "선발투수 3"}:
        pool = STARTERS
    elif slot in {"중간계투 1", "중간계투 2"}:
        pool = RELIEVERS
    elif slot == "마무리투수":
        pool = CLOSERS
    else:
        pool = [p for p in BATTERS if p["slot"] == slot]
    already_signed = set(roster.values())
    return [p for p in pool if p["id"] not in already_signed]


def team_power(roster: dict) -> float:
    if not roster:
        return 0.0
    ratings = [player_rating(PLAYER_BY_ID[player_id]) for player_id in roster.values()]
    return round(sum(ratings) / len(ratings), 1)


def reset_game():
    st.session_state.roster = {}
    st.session_state.spent = 0.0
    st.session_state.game_started = True
    st.session_state.team_name = st.session_state.get("team_name_input", "나만의 드림팀")
    st.session_state.initial_budget = st.session_state.get("budget_input", 100)
    # selectbox 위젯 선택 상태도 초기화
    for key in list(st.session_state.keys()):
        if key.startswith("pick_"):
            del st.session_state[key]


st.set_page_config(page_title="나만의 KBO 드림팀 만들기", page_icon="⚾", layout="wide")
st.title("⚾ 나만의 KBO 드림팀 만들기")
st.markdown("실제 KBO 구단 선수들을 성적에 따른 게임 머니로 영입해 나만의 팀을 완성해 보세요!")
st.caption("2026 KBO 정규시즌 기록 기반 · 9명 타선 + 선발 3명 + 중간계투 2명 + 마무리 1명")

with st.sidebar:
    st.header("게임 설정")
    st.text_input("팀 이름", value="나만의 드림팀", key="team_name_input")
    st.selectbox("시작 예산", [80, 90, 100, 110, 120], index=2, format_func=lambda x: f"{x}억 원", key="budget_input")
    st.markdown("**게임 규칙**")
    st.markdown("- 포지션마다 선수 1명 영입\n- 같은 선수는 중복 영입 불가\n- 예산을 초과하면 영입 불가\n- 선수 방출 시 영입가를 돌려받음")
    st.button("새 게임 시작 / 초기화", on_click=reset_game, use_container_width=True)

if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "roster" not in st.session_state:
    st.session_state.roster = {}
if "spent" not in st.session_state:
    st.session_state.spent = 0.0
if "initial_budget" not in st.session_state:
    st.session_state.initial_budget = 100
if "team_name" not in st.session_state:
    st.session_state.team_name = "나만의 드림팀"

# 아직 영입한 선수가 없다면 사이드바 설정 변경을 바로 반영
if not st.session_state.roster:
    st.session_state.initial_budget = st.session_state.get("budget_input", 100)
    st.session_state.team_name = st.session_state.get("team_name_input", "나만의 드림팀")
st.session_state.game_started = True

budget = float(st.session_state.initial_budget)
remaining = round(budget - st.session_state.spent, 1)

# 상단 현황
m1, m2, m3, m4 = st.columns(4)
m1.metric("팀 예산", f"{budget:.1f}억")
m2.metric("사용 금액", f"{st.session_state.spent:.1f}억")
m3.metric("남은 금액", f"{remaining:.1f}억")
m4.metric("영입 인원", f"{len(st.session_state.roster)} / {len(SLOTS)}명")
st.progress(len(st.session_state.roster) / len(SLOTS))

st.subheader(f"🏟️ {st.session_state.team_name} 선수 영입 시장")
st.write("각 포지션의 후보를 살펴보고 **영입하기**를 눌러 선수를 데려오세요. 선수의 가격은 화면에 표시된 2026 성적을 게임 가격 공식에 넣어 계산합니다.")

# 각 슬롯별 영입 UI
for slot_index, slot in enumerate(SLOTS):
    current_id = st.session_state.roster.get(slot)
    with st.expander(f"{'✅' if current_id else '⬜'} {slot}  {'- 영입 완료' if current_id else '- 선수 선택'}", expanded=(current_id is None)):
        if current_id:
            player = PLAYER_BY_ID[current_id]
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{player['name']}** · {player['team']}")
                st.caption(format_player_stats(player))
            with col2:
                st.metric("영입가", f"{player_price(player):.1f}억 원")
            with col3:
                if st.button("방출", key=f"release_{slot_index}", use_container_width=True):
                    st.session_state.spent = round(st.session_state.spent - player_price(player), 1)
                    del st.session_state.roster[slot]
                    pick_key = f"pick_{slot_index}"
                    if pick_key in st.session_state:
                        del st.session_state[pick_key]
                    st.rerun()
        else:
            available = get_available_players(slot, st.session_state.roster)
            if not available:
                st.warning("현재 영입 가능한 선수가 없습니다.")
            else:
                labels = {
                    p["id"]: f"{p['name']} ({p['team']}) | {player_price(p):.1f}억"
                    for p in available
                }
                pick_col, info_col, button_col = st.columns([3, 3, 1.2])
                with pick_col:
                    selected_id = st.selectbox(
                        "영입할 선수",
                        options=[p["id"] for p in available],
                        format_func=lambda pid: labels[pid],
                        key=f"pick_{slot_index}",
                    )
                selected_player = PLAYER_BY_ID[selected_id]
                with info_col:
                    st.caption(format_player_stats(selected_player))
                    st.caption(f"예상 전력 점수: {player_rating(selected_player):.1f}점")
                with button_col:
                    st.write("")
                    if st.button("영입하기", key=f"sign_{slot_index}", type="primary", use_container_width=True):
                        cost = player_price(selected_player)
                        if cost > remaining:
                            st.error(f"예산이 부족합니다. {cost:.1f}억 원이 필요합니다.")
                        elif selected_id in st.session_state.roster.values():
                            st.error("이미 영입한 선수입니다.")
                        else:
                            st.session_state.roster[slot] = selected_id
                            st.session_state.spent = round(st.session_state.spent + cost, 1)
                            st.rerun()

# 현재 팀 구성
st.divider()
st.subheader("📋 현재 우리 팀")
if st.session_state.roster:
    lineup_rows = []
    for slot in SLOTS:
        player_id = st.session_state.roster.get(slot)
        if player_id:
            p = PLAYER_BY_ID[player_id]
            lineup_rows.append({
                "포지션": slot,
                "선수": p["name"],
                "소속 구단": p["team"],
                "주요 성적": format_player_stats(p),
                "영입가(억)": player_price(p),
            })
    st.dataframe(pd.DataFrame(lineup_rows), use_container_width=True, hide_index=True)
else:
    st.info("아직 영입한 선수가 없습니다. 위 선수 영입 시장에서 첫 선수를 선택해 보세요!")

# 완성 팀 결과
if len(st.session_state.roster) == len(SLOTS):
    st.balloons()
    power = team_power(st.session_state.roster)
    st.success(f"🎉 축하합니다! {st.session_state.team_name}의 15인 로스터가 완성됐습니다!")
    r1, r2, r3 = st.columns(3)
    r1.metric("팀 전력 점수", f"{power:.1f} / 100")
    r2.metric("총 영입 비용", f"{st.session_state.spent:.1f}억 원")
    r3.metric("남은 예산", f"{remaining:.1f}억 원")
    if power >= 90:
        st.markdown("### 🏆 최상급 드림팀! 포지션별 전력이 매우 높습니다.")
    elif power >= 85:
        st.markdown("### ⭐ 강력한 우승 후보 팀입니다!")
    elif power >= 80:
        st.markdown("### 💪 균형 잡힌 경쟁력 있는 팀입니다!")
    else:
        st.markdown("### ⚾ 팀 완성! 다음에는 선수 구성을 바꿔 더 높은 전력에 도전해 보세요.")
else:
    st.caption(f"팀 완성까지 {len(SLOTS) - len(st.session_state.roster)}명 남았습니다.")

with st.expander("💡 선수 가격과 전력 점수 계산 방법"):
    st.markdown("""
    이 게임의 영입가는 실제 계약 연봉이나 시장 가치가 아닙니다. 실제 2026 정규시즌 성적을 단순한 게임 규칙으로 바꾼 **가상 가격**입니다.

    - 타자: `3.0 + OPS × 5.0` (억 원)
    - 선발투수: `2.0 + (5.0 - ERA) × 0.9 + 이닝 ÷ 250 + 탈삼진 ÷ 250` (억 원)
    - 중간계투: `2.5 + 홀드 × 0.12` (억 원)
    - 마무리투수: `3.0 + 세이브 × 0.10` (억 원)

    전력 점수는 선수 간 비교와 게임 결과 표시를 위한 별도 점수이며, 공식 KBO 지표나 선수의 실제 능력 평가와 같지 않습니다.
    """)

with st.expander("📚 데이터 출처 및 기준"):
    st.write("데이터 기준: 2026 KBO 정규시즌 종료 기록. 포지션별 타자 후보는 해당 시즌 가장 많이 출전한 수비 위치를 기준으로 정리된 OPS 상위 선수들입니다.")
    for label, url in SOURCES.items():
        st.markdown(f"- [{label}]({url})")
    st.caption("구단·포지션·기록은 2026시즌 기준입니다. 다음 시즌으로 넘어가면 선수 소속이나 기록이 바뀔 수 있습니다.")

st.caption("팬 게임용 선수 영입 시뮬레이터 · 실제 KBO 구단과 선수 기록을 참고했으며, KBO 공식 게임 또는 구단 서비스는 아닙니다.")
