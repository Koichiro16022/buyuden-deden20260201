import streamlit as st
import google.generativeai as genai
import random

# API/Model設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝", page_icon="💃")

# CSS: オチの表示ボックス用
st.markdown("<style>.ochi-box {background:#f0f2f6; padding:15px; border-radius:10px; border-left:5px solid #ff4b4b; margin-bottom:20px;}</style>", unsafe_allow_html=True)

st.title("💃 武勇伝デデン")

# セッション初期化
if 'step' not in st.session_state: st.session_state.step = 1
if 'ochi_list' not in st.session_state: st.session_state.ochi_list = []
if 'furi_list' not in st.session_state: st.session_state.furi_list = []
if 'kw' not in st.session_state: st.session_state.kw = "空手"

kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻", "職質", "確定申告", "推し活", "二度寝", "自撮り", "婚活"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader("① キーワード入力")
    # vertical_alignment="bottom" で入力欄とボタンの底を揃える
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    with c1: 
        val = st.text_input("", value=st.session_state.kw)
    with c2: 
        if st.button("ランダム", use_container_width=True):
            st.session_state.kw = random.choice(kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        with st.spinner("思考中..."):
            p = f"慎吾として「{val}」のオチを20案。ひらがな、4/4/5、スラッシュ区切り。データのみ。"
            try:
                r = model.generate_content(p)
                st.session_state.ochi_list = [l.strip() for l in r.text.split('\n') if '/' in l][:20]
                st.session_state.step = 2
                st.rerun()
            except Exception as e: st.error(f"ERR: {e}")

# --- STEP 2 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾のオチを選択")
    if st.session_state.ochi_list:
        sel = st.selectbox("案", st.session_state.ochi_list)
        st.session_state.f_ochi = st.text_input("修正", value=sel)
        if st.button("振りを20案出す", use_container_width=True, type="primary"):
            with st.spinner("思考中..."):
                p = f"中田として「{st.session_state.f_ochi}」への振りを20案。ひらがな、4/4/5、スラッシュ区切り。"
                try:
                    r = model.generate_content(p)
                    st.session_state.furi_list = [l.strip() for l in r.text.split('\n') if '/' in l][:20]
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e: st.error(f"ERR: {e}")
        if st.button("戻る"):
            st.session_state.step = 1
            st.rerun()

# --- STEP 3 ---
elif st.session_state.step == 3:
    st.markdown(f'<div class="ochi-box">し：すごい！ {st.session_state.f_ochi}</div>', unsafe_allow_html=True)
    st.subheader("③ あっちゃんの振りを選択")
    if st.session_state.furi_list:
        sel = st.selectbox("案", st.session_state.furi_list)
        st.session_state.f_furi = st.text_input("修正", value=sel)
        if st.button("完成！", use_container_width=True, type="primary"):
            st.session_state.step = 4
            st.rerun()
        if st.button("戻る"):
            st.session_state.step = 2
            st.rerun()

# --- FINAL ---
elif st.session_state.step == 4:
    st.success("伝説完成！")
    st.markdown("---")
    st.markdown(f"### **あ：{st.session_state.f_furi}**")
    st.markdown(f"### **し：すごい！ {st.session_state.f_ochi}**")
    st.markdown("### **＼ デデン
