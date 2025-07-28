import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_CREDENTIAL_PATH")

def initialize_firestore():
    if not SERVICE_ACCOUNT_PATH or not os.path.exists(SERVICE_ACCOUNT_PATH):
        raise FileNotFoundError(f"❌ サービスアカウントファイルが見つかりません。現在の設定: {SERVICE_ACCOUNT_PATH}")

    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
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

    doc_ref = db.collection("user_histories").document(user_id)
    doc_ref.delete()