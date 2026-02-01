import streamlit as st
import google.generativeai as genai
import random

# API/Model設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# --- 日本語ラベル（断線防止用） ---
L_STEP1 = "① キーワード入力"
L_STEP2 = "② 慎吾のオチを選択"
L_STEP3 = "③ あっちゃんの振りを選択"
L_MSG = "＼ デデンデンデンデン！ ／"

st.set_page_config(page_title="武勇伝", page_icon="💃")
st.markdown("<style>.ochi-box {background:#f0f2f6; padding:15px; border-radius:10px; border-left:5px solid #ff4b4b; margin-bottom:20px;}</style>", unsafe_allow_html=True)
st.title("💃 武勇伝デデン")

# セッション初期化
if 'step' not in st.session_state: st.session_state.step = 1
if 'o_list' not in st.session_state: st.session_state.o_list = []
if 'f_list' not in st.session_state: st.session_state.f_list = []
if 'kw' not in st.session_state: st.session_state.kw = "空手"

kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻", "確定申告"]

# --- STEP 1: オチ生成 ---
if st.session_state.step == 1:
    st.subheader(L_STEP1)
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    with c1: val = st.text_input("", value=st.session_state.kw)
    with c2: 
        if st.button("ガチャ"):
            st.session_state.kw = random.choice(kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        with st.spinner("思考中..."):
            prompt = f"慎吾として「{val}」のオチ20案。ひらがな、4/4/5、スラッシュ区切り。データのみ。"
            try:
                # 確実にレスポンスを受け取るためのシンプル処理
                res = model.generate_content(prompt)
                st.session_state.o_list = [l.strip() for l in res.text.split('\n') if '/' in l][:20]
                st.session_state.step = 2
                st.rerun()
            except:
                st.error("AIが恥ずかしがっています。もう一度押してください。")

# --- STEP 2: 振り生成 ---
elif st.session_state.step == 2:
    st.subheader(L_STEP2)
    if st.session_state.o_list:
        sel_o = st.selectbox("案", st.session_state.o_list)
        st.session_state.f_o = st.text_input("修正", value=sel_o)
        
        if st.button("振りを20案出す", use_container_width=True, type="primary"):
            with st.spinner("思考中..."):
                prompt_f = f"中田として「{st.session_state.f_o}」への振り20案。ひらがな、4/4/5、スラッシュ区切り。"
                try:
                    res_f = model.generate_content(prompt_f)
                    st.session_state.f_list = [l.strip() for l in res_f.text.split('\n') if '/' in l][:20]
                    st.session_state.step = 3
                    st.rerun()
                except:
                    st.error("中田がカッコつけすぎています。もう一度押してください。")
        if st.button("戻る"):
            st.session_state.step = 1
            st.rerun()

# --- STEP 3: 完成確認 ---
elif st.session_state.step == 3:
    st.markdown(f'<div class="ochi-box">し：すごい！ {st.session_state.f_o}</div>', unsafe_allow_html=True)
    st.subheader(L_STEP3)
    if st.session_state.f_list:
        sel_f = st.selectbox("案", st.session_state.f_list)
        st.session_state.f_f = st.text_input("修正", value=sel_f)
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
    st.markdown(f"### **あ：{st.session_state.f_f}**")
    st.markdown(f"### **し：すごい！ {st.session_state.f_o}**")
    st.markdown(f"### **{L_MSG}**")
    st.markdown("---")
    if st.button("新しく作る", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
