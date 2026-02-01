import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])

# モデルの指定を「models/」付きに修正して安定性を高めます
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="武勇伝デデン", page_icon="💃")

st.title("💃 武勇伝デデン")
st.caption("AIの量と人間の質で創る、あなただけの武勇伝")

# セッション状態の初期化
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"

# ランダムキーワードのリスト
random_kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "キャンプ", "遅刻", "ダイエット"]

# --- STEP 1: キーワード入力 ---
if st.session_state.step == 1:
    st.subheader("① キーワードを入力")
    
    col_kw, col_rnd = st.columns([4, 1])
    with col_kw:
        kw = st.text_input("どんなネタにしますか？", value=st.session_state.kw_value)
    with col_rnd:
        st.write(" ") # 余白調整
        if st.button("ランダム"):
            st.session_state.kw_value = random.choice(random_kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True):
        with st.spinner("慎吾が必死に考えています..."):
            try:
                prompt = f"オリエンタルラジオの武勇伝ネタを作ります。キーワード「{kw}」を使って、慎吾の『情けないオチ』を「〇〇(4) / 〇〇(4) / 〇〇(5)」のリズムで20案出してください。解説や番号は不要。1行1案のリストのみ出力。"
                response = model.generate_content(prompt)
                st.session_state.ochi_list = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# --- STEP 2: オチ選択・修正 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾の「オチ」を選択・修正")
    selected_base_ochi = st.selectbox("AI案から選ぶ（4・4・5のリズム）", st.session_state.ochi_list)
    final_ochi = st.text_input("ここでオチを自由に修正してください", value=selected_base_ochi)
    st.session_state.final_ochi = final_ochi

    col1, col2 = st.columns(2)
    with col1:
        if st.button("これで確定！振りを20案出す"):
            with st.spinner("あっちゃんがカッコつけて考えています..."):
                try:
                    prompt = f"武勇伝ネタ。オチ「{final_ochi}」に繋がる、あっちゃんの『強気な振り』を「〇〇(4) / 〇〇(4) / 〇〇(5)」のリズムで20案出してください。解説や番号は不要。1行1案のリストのみ出力。"
                    response = model.generate_content(prompt)
                    st.session_state.furi_list = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
    with col2:
        if st.button("キーワード入力に戻る"):
            st.session_state.step = 1
            st.rerun()

# --- STEP 3: 振り選択・修正 ---
elif st.session_state.step == 3:
    st.subheader("③ あっちゃんの「振り」を選択・修正")
    selected_base_furi = st.selectbox("AI案から選ぶ（4・4・5のリズム）", st.session_state.furi_list)
    final_furi = st.text_input("ここで振りを自由に修正してください", value=selected_base_furi)
    st.session_state.final_furi = final_furi

    col1, col2 = st.columns(2)
    with col1:
        if st.button("武勇伝を完成させる！"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("オチの選択に戻る"):
            st.session_state.step = 2
            st.rerun()

# --- FINAL: 結果表示 ---
elif st.session_state.step == 4:
    st.balloons()
    st.success("伝説完成！")
    st.markdown("---")
    st.markdown(f"### **あ：{st.session_state.final_furi}**")
    st.markdown(f"### **し：すごい！ {st.session_state.final_ochi}**")
    st.markdown("### **＼ デンデンデデンデン！ ／**")
    st.markdown("---")
    if st.button("新しいネタを作る"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
