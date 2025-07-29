import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

try:
    import streamlit as st
    STREAMLIT = True
except ImportError:
    STREAMLIT = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_CREDENTIAL_PATH")

def initialize_firestore():
    if not firebase_admin._apps:
        if SERVICE_ACCOUNT_PATH and os.path.exists(SERVICE_ACCOUNT_PATH):
            # ✅ ローカル環境（.env 経由）
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        elif STREAMLIT and "FIREBASE_SERVICE_ACCOUNT" in st.secrets:
            # ✅ Streamlit Cloud 環境（secrets.toml 経由）
            service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
            cred = credentials.Certificate(service_account_info)
        else:
            raise FileNotFoundError(f"❌ Firebaseのサービスアカウント情報が見つかりません。")

        firebase_admin.initialize_app(cred)

    return firestore.client()

def save_user_history(db, user_id, new_entry):
    if not user_id or not new_entry:
        return

    doc_ref = db.collection("user_histories").document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        existing_history = doc.to_dict().get("history", [])
    else:
        existing_history = []

    existing_history.append(new_entry)
    doc_ref.set({"history": existing_history})

def load_user_history(db, user_id):
    if not user_id:
        return []

    doc_ref = db.collection("user_histories").document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict().get("history", [])
    else:
        return []

def clear_user_history(db, user_id):
    if not user_id:
        return

    db.collection("user_histories").document(user_id).delete()
