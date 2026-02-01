import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝デデン", page_icon="💃")

# CSS調整
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
    </style>
    """, unsafe_allow_html=True)

st.title("💃 武勇伝デデン")

# セッション状態の初期化
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
    "プログラミング", "デバッグ", "プレゼン", "飲み会", "二度寝", "SNS", "サウナ", "宝くじ", "婚活", "美容整形"
]

# --- STEP 1 ---
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
        with st.spinner("思考中..."):
            try:
                # 1行が長くならないように分割
                p = f"キーワード「{kw}」で情けないオチを20案出せ。"
                p += "ルール：1.ひらがなのみ。2.「4/4/5」のリズム。"
                p += "3.スラッシュ区切り。4.20案のリストのみ。"
                response = model.generate_content(p)
                st.session_state.ochi_list = [l.strip() for l in response.text.strip().split('\n') if l.strip()]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"エラー: {e}")

# --- STEP 2 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾の「オチ」を選択・修正")
    if st.session_state.ochi_list:
        selected_ochi = st.selectbox("AI案（ひらがな 4/4/5）", st.session_state.ochi_list)
        final_ochi = st.text_input("オチを修正", value=selected_ochi)
        st.session_state.final_ochi = final_ochi

        c1, c2 = st.columns(2)
        with c1:
            if st.button("振りを20案出す", use_container_width=True, type="primary"):
                with st.spinner("思考中..."):
                    p = f"オチ「{final_ochi}」に繋がる強気な振りを20案出せ。"
                    p += "ルール：1.ひらがなのみ。2.「4/4/5」のリズム。"
                    p += "3.スラッシュ区切り。4.20案のリストのみ。"
                    response = model.generate_content(p)
                    st.session_state.furi_list = [l.strip() for l in response.text.strip().split('\n') if l.strip()]
                    st.session_state.step = 3
                    st.rerun()
        with c2:
            if st.button("戻る", use_container_width=True):
                st.session_state.step = 1
                st.rerun()

# --- STEP 3 ---
elif st.session_state.step == 3:
    st.markdown(f'<div class="ochi-display">し：すごい！ {st.session_state.final_ochi}</div>', unsafe_allow_html=True)
    st.subheader("③ あっちゃんの「振り」を選択・修正")
    if st.session_state.furi_list:
        selected_furi = st.selectbox("AI案（ひらがな 4/4/5）", st.session_state.furi_list)
        final_furi = st.text_input("振りを修正", value=selected_furi)
        st.session_state.final_furi = final_furi

        c1, c2 = st.columns(2)
        with c1:
            if st.button("完成！", use_container_width=True, type="primary"):
                st.session_state.step = 4
                st.rerun()
        with c2:
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
    if st.button("新しく作る", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
