import streamlit as st
import google.generativeai as genai

st.title("🧪 Gemini モデル診断")

# API設定
try:
    genai.configure(api_key=st.secrets["api_key"])
    
    st.write("### 1. 接続テスト")
    # 利用可能なモデルをリストアップ
    models = genai.list_models()
    model_list = []
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            model_list.append(m.name)
    
    if model_list:
        st.success("APIキーは正しく認識されています！")
        st.write("### 2. あなたの環境で使えるモデル名一覧")
        st.info("以下の名称のいずれかをコードに記述する必要があります。")
        st.write(model_list)
        
        # 簡易テスト
        st.write("### 3. 疎通テスト (gemini-1.5-flash)")
        test_model_name = 'models/gemini-1.5-flash' # リストにある名前に合わせて書き換える
        if st.button("このモデルでテスト送信"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("「武勇伝」と一言返してください。")
            st.write("AIからの返信:", response.text)
    else:
        st.warning("利用可能なモデルが見つかりませんでした。")

except Exception as e:
    st.error(f"致命的なエラーが発生しました: {e}")

if st.button("診断終了（元のアプリに戻る準備）"):
    st.write("上のリストにある名前を教えてください！")
