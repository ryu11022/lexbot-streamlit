import streamlit as st
import os
from PIL import Image
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr
import requests
from google.api_core.exceptions import ResourceExhausted
import html
from datetime import datetime
now = datetime.now()

# --- デバッグ: Secretsに何のキーがあるか確認 ---
st.write("Secrets keys (本番):", list(st.secrets.keys()))

api_key = st.secrets.get("GEMINI_API_KEY")

# ローカル用のフォールバック
if not api_key:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

# デバッグ表示
st.write("APIキー取得結果:", bool(api_key))

if not api_key:
    st.error("Gemini API Key が設定されていません。")
    st.stop()  # APIキーなしなら強制終了
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

st.title("LexBot")
direction_label = {"en-to-ja": "英語から日本語", "ja-to-en": "日本語から英語"}
