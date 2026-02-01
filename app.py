import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
m_name = 'models/gemini-flash-latest'
model = genai.GenerativeModel(m_name)

st.set_page_config(page_title="武勇伝", page_icon="💃")

# CSS
style = "<style>div[data-testid='stColumn'] > div > div > div > button "
style += "{margin-top: 28px !important;} .ochi-display "
style += "{background-color: #f0f2f6; padding: 15px; border-radius: 10px; "
style += "border-left: 5px solid #ff4b4b; margin-bottom: 20px;}</style>"
st.markdown(style, unsafe_allow_html=True)

st.title("💃 武勇伝デデン")

# 初期化
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"

kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader("① キーワード")
    t_list = ["エンジニア", "経理", "営業", "品質管理"]
    target = st.selectbox("ターゲット", t_list)
    
    c1, c2 = st.columns([3, 1])
    with c1:
        kw = st.text_input("ネタの種", value=st.session_state.kw_value)
    with c2:
        if st.button("ガチャ"):
            st.session_state.kw_value = random.choice(kws)
            st.rerun()
    
    if st.button("オチを出す", use_container_width=True, type="primary"):
        with st.spinner("思考中..."):
            p = f"{kw}の{target}向けオチを20案。ひらがなのみ。"
            p += "リズムは4/4/5。スラッシュ区切り。リストのみ出力。"
            try:
                res = model.generate_content(p)
                st.session_state.ochi_list = [l.strip() for l in res.text.split('\n') if l.strip()]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"ERR: {e}")

# --- STEP 2 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾のオチ")
    if st.session_state.ochi_list:
        sel_ochi = st.selectbox("AI案を選択", st.session_state.ochi_list)
        st.session_state.final_ochi = st.text_input("修正", value=sel_ochi)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("振りを出す", use_container_width=True, type="primary"):
                with st.spinner("思考中..."):
                    fp = f"オチ「{st.session_state.final_ochi}」への強気な振りを20案。"
                    fp += "ひらがなのみ。リズム4/4/5。スラッシュ区切り。リストのみ。"
                    try:
                        res_f = model.generate_content(fp)
                        st.session_state.furi_list = [l.strip() for l in res_f.text.split('\n') if l.strip()]
                        st.session_state.step = 3
                        st.rerun()
                    except Exception as e
