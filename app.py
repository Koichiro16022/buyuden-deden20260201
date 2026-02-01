import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝", page_icon="💃")

# CSS
st.markdown("<style>div[data-testid='stColumn'] > div > div > div > button {margin-top: 28px !important;} .ochi-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;}</style>", unsafe_allow_html=True)

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

# --- STEP 1: キーワード入力 ---
if st.session_state.step == 1:
    st.subheader("① キーワード入力")
    c1, c2 = st.columns([3, 1])
    with c1:
        kw = st.text_input("ネタの種（何について？）", value=st.session_state.kw_value)
    with c2:
        if st.button("ランダム"):
            st.session_state.kw_value = random.choice(kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        with st.spinner("慎吾がリズムを刻んでいます..."):
            p = f"オリラジ慎吾として、キーワード「{kw}」の情けないオチを20案出せ。"
            p += "【厳守】1.ひらがなのみ 2.4/4/5のリズム 3.スラッシュ区切り "
            p += "4.解説、タイトル、凡例は一切禁止。データのみ20行出力せよ。"
            try:
                res = model.generate_content(p)
                # 不純物（記号や空行）を徹底除去
                lines = [l.strip() for l in res.text.split('\n') if '/' in l]
                st.session_state.ochi_list = lines[:20]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"ERR: {e}")

# --- STEP 2: オチ選択 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾のオチを選択")
    if st.session_state.ochi_list:
        sel_o = st.selectbox("案を選択", st.session_state.ochi_list)
        st.session_state.final_ochi = st.text_input("修正", value=sel_o)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("振りを20案出す", use_container_width=True, type="primary"):
                with st.spinner("あっちゃんがカッコつけています..."):
                    # 振りのプロンプトにもスラッシュ区切りを徹底
                    fp = f"オリラジ中田として、オチ「{st.session_state.final_ochi}」への強気な振りを20案出せ。"
                    fp += "【厳守】1.ひらがなのみ 2.4/4/5のリズム 3.スラッシュ区切り "
                    fp += "4.解説、凡例、タイトルは一切不要。データのみ20行出力せよ。"
                    try:
                        res_f = model.generate_content(fp)
                        # スラッシュが含まれる行のみを抽出してリスト化
                        f_lines = [l.strip() for l in res_f.text.split('\n') if '/' in l]
                        st.session_state.furi_list = f_lines[:20]
                        st.session_state.step = 3
                        st.rerun()
                    except Exception as e:
                        st.error(f"ERR: {e}")
        with c2:
            if st.button("戻る", use_container_width=True):
                st.session_state.step = 1
                st.rerun()

# --- STEP 3: 振り選択 ---
elif st.session_state.step == 3:
    st.markdown(f'<div class="ochi-box">し：すごい！ {st.session_state.final_ochi}</div>', unsafe_allow_html=True)
    st.subheader("③ あっちゃんの振りを選択")
    if st.session_state.furi_list:
        sel_f = st.selectbox("案を選択", st.session_state.furi_list)
        st.session_state.final_furi = st.text_input("修正", value=sel_f)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("完成！", use_container_width=True, type="primary"):
                st.session_state.step = 4
                st.rerun()
        with c2:
            if st.button("戻る", use_container_width=True):
                st.session_state.step = 2
                st.rerun()

# --- FINAL: 結果 ---
elif st.session_state.step == 4:
    st.success("伝説完成！")
    st.markdown("---")
    # ここでもリズムよく表示
    st.markdown(f"### **あ：{st.session_state.final_furi}**")
    st.markdown(f"### **し：すごい！ {st.session_state.final_ochi}**")
    st.markdown("### **＼ デデンデンデンデン！ ／**")
    if st.button("新しく作る", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
