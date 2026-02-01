import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝デデン", page_icon="💃")

# CSSでレイアウトと色を調整
st.markdown("""
    <style>
    div[data-testid="stColumn"] > div > div > div > button {
        margin-top: 28px !important;
    }
    .ochi-display {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .furi-label { color: #1f77b4; font-weight: bold; }
    .ochi-label { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("💃 武勇伝デデン")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"
if 'final_ochi' not in st.session_state:
    st.session_state.final_ochi = ""

random_kws = [
    "空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "キャンプ", "遅刻", "ダイエット",
    "プログラミング", "デバッグ", "プレゼン", "飲み会", "二度寝", "SNS", "サウナ", "宝くじ", "婚活", "美容整形",
    "リモートワーク", "残業", "確定申告", "お化け屋敷", "スカイダイビング", "英会話", "一人カラオケ", "食べ放題", "断捨離", "推し活"
]

# --- STEP 1: キーワード入力 ---
if st.session_state.step == 1:
    st.subheader("① キーワードを入力")
    col_kw, col_rnd = st.columns([3, 1])
    with col_kw:
        kw = st.text_input("どんなネタにしますか？", value=st.session_state.kw_value)
    with col_rnd:
        if st.button("ランダム", use_container_width=True):
            st.session_state.kw_value = random.choice(random_kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        with st.spinner("慎吾が必死に20案考えています..."):
            try:
                prompt = f"オリエンタルラジオの武勇伝ネタ。キーワード「{kw}」で、慎吾の『情けないオチ』を「4・4・5」のリズムで必ず20案。1行1案、解説不要。"
                response = model.generate_content(prompt)
                st.session_state.ochi_list = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"エラー: {e}")

# --- STEP 2: オチ選択・修正 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾の「オチ」を選択・修正")
    selected_base_ochi = st.selectbox(f"AI案（全{len(st.session_state.ochi_list)}案）", st.session_state.ochi_list)
    final_ochi = st.text_input("ここでオチを自由に修正してください", value=selected_base_ochi)
    st.session_state.final_ochi = final_ochi

    col1, col2 = st.columns(2)
    with col1:
        if st.button("これで確定！振りを20案出す", use_container_width=True, type="primary"):
            with st.spinner("中田敦彦がカッコつけて20案考えています..."):
                prompt = f"武勇伝。オチ「{final_ochi}」に繋がる、あっちゃんの『強気な振り』を「4・4・5」のリズムで必ず20案。1行1案、解説不要。"
                response = model.generate_content(prompt)
                st.session_state.furi_list = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
                st.session_state.step = 3
                st.rerun()
    with col2:
        if st.button("戻る", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# --- STEP 3: 振り選択・修正 ---
elif st.session_state.step == 3:
    # 【追加機能】確定したオチを常に表示
    st.markdown(f"""
        <div class="ochi-display">
            <span class="ochi-label">【確定したオチ】</span><br>
            <h3 style="margin:0;">し：すごい！ {st.session_state.final_ochi}</h3>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("③ あっちゃんの「振り」を選択・修正")
    selected_base_furi = st.selectbox(f"AI案（全{len(st.session_state.furi_list)}案）", st.session_state.furi_list)
    final_furi = st.text_input("ここで振りを自由に修正してください", value=selected_base_furi)
    st.session_state.final_furi = final_furi

    col1, col2 = st.columns(2)
    with col1:
        if st.button("武勇伝を完成させる！", use_container_width=True, type="primary"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("戻る", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# --- FINAL ---
elif st.session_state.step == 4:
    st.balloons()
    st.success("伝説完成！")
    st.markdown("---")
    st.markdown(f"### **あ：{st.session_state.final_furi}**")
    st.markdown(f"### **し：すごい！ {st.session_state.final_ochi}**")
    st.markdown("### **＼ デンデンデデンデン！ ／**")
    st.markdown("---")
    if st.button("新しいネタを作る", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
