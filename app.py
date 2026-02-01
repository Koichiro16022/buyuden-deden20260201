import streamlit as st
import google.generativeai as genai
import random

# API設定：1.5 Flash 相当の安定版を指定
genai.configure(api_key=st.secrets["api_key"])
# 混雑に強く、爆速で動く安定モデルを指定
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝デデン", page_icon="💃")

# CSSでボタンの位置をミリ単位で調整
st.markdown("""
    <style>
    div[data-testid="stColumn"] > div > div > div > button {
        margin-top: 28px !important;
    }
    .stButton>button {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💃 武勇伝デデン")
st.caption("安定のFlashモデルで爆速生成、あなただけの武勇伝")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"

random_kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "キャンプ", "遅刻", "ダイエット"]

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
        with st.spinner("慎吾が爆速で考えています..."):
            try:
                # 4・4・5のリズムをより厳格に守らせるための微調整
                prompt = f"オリエンタルラジオの武勇伝ネタ。キーワード「{kw}」で、慎吾の『情けないオチ』を「〇〇(4) / 〇〇(4) / 〇〇(5)」のリズムで20案。1行1案、解説不要、必ず20案。"
                response = model.generate_content(prompt)
                st.session_state.ochi_list = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"エラー: {e}")

# --- STEP 2: オチ選択・修正 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾の「オチ」を選択・修正")
    if st.session_state.ochi_list:
        selected_base_ochi = st.selectbox("AI案から選ぶ（4・4・5）", st.session_state.ochi_list)
        final_ochi = st.text_input("ここでオチを自由に修正してください", value=selected_base_ochi)
        st.session_state.final_ochi = final_ochi

        col1, col2 = st.columns(2)
        with col1:
            if st.button("これで確定！振りを20案出す", use_container_width=True, type="primary"):
                with st.spinner("あっちゃんがカッコつけて考えています..."):
                    prompt = f"武勇伝。オチ「{final_ochi}」に繋がる、あっちゃんの『強気な振り』を「〇〇(4) / 〇〇(4) / 〇〇(5)」のリズムで20案。1行1案、解説不要、必ず20案。"
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
    st.subheader("③ あっちゃんの「振り」を選択・修正")
    if st.session_state.furi_list:
        selected_base_furi = st.selectbox("AI案から選ぶ（4・4・5）", st.session_state.furi_list)
        final_furi = st.text_input("ここで振りを自由に修正してください", value=selected_base_furi)
        st.session_state.final_furi = final_furi

        col1, col2 = st.columns(2)
        with col1:
            if st.button("完成させる！", use_container_width=True, type="primary"):
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
    st.markdown(f"### **あ：{st.session_state.final_furi}**")
    st.markdown(f"### **し：すごい！ {st.session_state.final_ochi}**")
    st.markdown("### **＼ デンデンデデンデン！ ／**")
    if st.button("新しいネタを作る", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
