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

api_key = st.secrets.get("GEMINI_API_KEY")

# ローカル → .env から
if not api_key:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key が設定されていません。")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

st.title("LexBot")

# ラベル
direction_label = {"en-to-ja": "英語から日本語", "ja-to-en": "日本語から英語"}

# ==== 多言語対応用 ==== 
LANGUAGES = ["English", "日本語", "中文", "한국어", "Español"]
LANG_CODES = {
    "English": "en",
    "日本語": "ja",
    "中文": "zh",
    "한국어": "ko",
    "Español": "es",
}

if 'ui_lang' not in st.session_state:
    st.session_state.ui_lang = "English"
    

CODE_TO_LANG_LABELS = {
    "en": "English",
    "ja": "日本語",
    "zh": "中文",
    "ko": "한국어",
    "es": "Español",
}


# ==== UI文言管理 ====
ui_text = {
    "English": {
        "title": "LexBot",
        "input_method": "Select input method",
        "manual": "Enter manually",
        "camera": "Extract from image",
        "next": "Next",
        "card_front": "Front",
        "card_back": "Back",
        "flip": "Flip",
        "next_card": "Next",
        "back": "Back",
        "language_from": "Language you want to learn",
        "language_to": "Your language",
        "image_toggle": "Show image",
        "speak": "Speak",
        "Input by voice": "Input by voice",
        "test_settings": "Test Settings",
        "format": "Format",
        "context": "Context",
        "start_quiz": "Start Quiz",
        "input_words": "Enter words (separated by space or newline)",
        "add_words": "Add",
        "current_words": "Current word list:",
        "to_config": "Go to test settings",
        "camera_title": "📷 Capture words with camera",
        "extracted_words": "Extracted words:",
        "go_to_config": "Go to test settings",
        "show_image": "Show image",
        "history": "History",
        "no_history": "No history yet.",
        "review_all": "Retake this test",
        "review_wrong": "Review wrong answers only",
        "reset_all": "Reset all words",
        "remove_card": "Remove this card",
        "your_answer": "Your answer",
        "correct_answer": "Correct answer",
        "feedback": "Feedback",
        "overall_feedback": "Overall feedback",
        "start_over": "Start Over",
        "hint": "Hint",
        "settings": "Settings",
        "language_setting": "Language Setting",
        "select_language": "Select interface language",
        "selected_language": "Selected language:",
        "apply": "Apply",
        "cancel": "Cancel",
        "save": "Save",
        "close": "Close",
        "notebook": "My Wordbook",
        "no_words": "No words yet.",
        "delete": "Delete",
        "confirm_delete": "Are you sure you want to delete this word?",
        "word_meaning": "Meaning",
        "synonyms": "Synonyms",
        "antonyms": "Antonyms",
        "part_of_speech": "Part of Speech",
        "example_sentence": "Example sentence",
        "related_image": "Related Image",
        "created_at": "Added on",
        "add_to_notebook": "Add to Wordbook",
        "flashcards": "Flashcards",
        "no_flashcards": "No flashcards available",
        "practice_mode": "Practice Mode",
        "quiz_mode": "Quiz Mode",
        "show_answer": "Show Answer",
        "hide_answer": "Hide Answer",
        "next_flashcard": "Next Flashcard",
        "result_summary": "Test Result Summary",
        "correct_count": "Correct answers:",
        "wrong_count": "Wrong answers:",
        "review_summary": "Review Summary",
        "delete_word": "Delete Word",
        "history_description": "Your past quiz attempts will be shown here.",
        "redo_test": "Redo full test",
        "redo_incorrect": "Review incorrect answers only",
        "multiple-choice": "Multiple Choice",
        "written": "Written",
        "language-translation": "Translation",
        "fill-blank": "Fill in the Blank",
        "free-text": "Free Text",
        "Voice input": "Voice input",
        "Input from camera": "Input from camera",
        "Input from history": "Input from history",
        "enter_more_words": "Enter more words",
        "clear_history": "Clear history",
        "no_history_yet": "No history yet.", 
        "howto_title": "How to Use LexBot",
        "howto_1": "1️⃣ Add Vocabulary",
        "howto_1_desc": "- Choose 📘 or 📚 to input words\n- Input methods: ✍️ Manual, 📜 History",
        "howto_2": "2️⃣ Generate a Quiz (📘)",
        "howto_2_desc": "- Select format and language pair\n- Supports translation & fill-in-blank, written or multiple-choice",
        "howto_3": "3️⃣ Study with Flashcards (📚)",
        "howto_3_desc": "- Flip cards, choose translation language\n- Easily delete/reset words",
        "howto_4": "4️⃣ Review History (📜)",
        "howto_4_desc": "- Check past results\n- Retry only incorrect words",
        "see_howto": "How to Use",
        "welcome": "Welcome",
        "login": "🔐 Login",
        "logged_in_as": "✅ Logged in as: ",
        "logout": "Logout",
        "email": "📧 Email",
        "password": "🔑 Password",
        "login_with_email": "Login with Email",
        "login_failed": "Login failed: ",
        "guest_mode": "Guest mode active.",
        "login_with_email": "Login with Email",
        "logout": "Logout",
        "login_failed": "Login failed: ",
        "new_account_created": "Created new account for: ",
        "make_new_account": "Make New Account",
        "create_account": "Create Account",
        "account_created_successfully": " account successfully created.",
        "account_creation_failed": "This account is registered: ",
        "flashcard_all": "Flashcards from all words",
        "flashcard_incorrect": "Flashcards from incorrect answers",
        "no_vocab_warning": "Please enter some vocabulary words before starting the quiz.",
        "history_title": "Test History",
        "test": "Test",
        "score": "Score",
        "timestamp": "Date Taken",
        "questions": "Questions",
        "select_translation_language": "Select translation language",
        "reset_success": "All words have been reset",
        "deleted": "Deleted",
        "no_words_entered": "No words entered",
        "delete_word": "Delete word"
    },
    "日本語": {
        "title": "LexBot",
        "input_method": "単語の入力方法を選んでください",
        "manual": "手動で入力",
        "camera": "画像から抽出",
        "next": "次へ",
        "card_front": "表面",
        "card_back": "裏面",
        "flip": "裏返す",
        "next_card": "次へ",
        "back": "戻る",
        "language_from": "学びたい言語",
        "language_to": "あなたの言語",
        "image_toggle": "画像を表示する",
        "speak": "音声で読む",
        "Input by voice": "音声で入力",
        "test_settings": "テスト設定",
        "format": "形式",
        "context": "文脈",
        "start_quiz": "テスト開始",
        "input_words": "単語を入力（スペースや改行で複数可）",
        "add_words": "追加",
        "current_words": "現在の単語リスト:",
        "to_config": "テスト設定へ",
        "camera_title": "📷 カメラで単語を読み取る",
        "extracted_words": "抽出された単語:",
        "go_to_config": "テスト設定へ",
        "show_image": "画像を表示する",
        "history": "履歴",
        "no_history": "まだ履歴がありません。",
        "review_all": "この単語テストをやりなおす",
        "review_wrong": "間違えた問題のみをやりなおす",
        "reset_all": "すべての単語をリセット",
        "remove_card": "このカードを削除",
        "score": "スコア",
        "your_answer": "あなたの回答",
        "correct_answer": "正解",
        "feedback": "フィードバック",
        "overall_feedback": "総合フィードバック",
        "start_over": "最初からやり直す",
        "hint": "ヒント",
        "settings": "設定",
        "language_setting": "言語設定",
        "select_language": "インターフェースの言語を選択",
        "selected_language": "選択中の言語:",
        "apply": "適用",
        "cancel": "キャンセル",
        "save": "保存",
        "close": "閉じる",
        "notebook": "自分の単語帳",
        "no_words": "まだ単語が登録されていません。",
        "delete": "削除",
        "confirm_delete": "この単語を削除しますか？",
        "word_meaning": "意味",
        "synonyms": "類義語",
        "antonyms": "対義語",
        "part_of_speech": "品詞",
        "example_sentence": "例文",
        "related_image": "関連画像",
        "created_at": "追加日時",
        "add_to_notebook": "単語帳に追加",
        "flashcards": "フラッシュカード",
        "no_flashcards": "フラッシュカードがありません",
        "practice_mode": "練習モード",
        "quiz_mode": "テストモード",
        "show_answer": "答えを表示",
        "hide_answer": "答えを隠す",
        "next_flashcard": "次のカード",
        "result_summary": "テスト結果のまとめ",
        "correct_count": "正解数:",
        "wrong_count": "不正解数:",
        "review_summary": "復習のまとめ",
        "delete_word": "単語を削除",
        "history_description": "これまでのクイズ結果がここに表示されます。",
        "redo_test": "テストをやり直す",
        "redo_incorrect": "間違えた問題のみ復習",
        "multiple-choice": "選択式",
        "written": "記述式",
        "language-translation": "翻訳問題",
        "fill-blank": "空欄補充",
        "free-text": "記述式",
        "Voice input": "音声入力",
        "Input from camera": "カメラから入力",
        "Input from history": "履歴から入力",
        "enter_more_words": "単語を追加で入力する",
        "clear_history": "履歴を削除",
        "no_history_yet": "まだ履歴がありません。",
        "howto_title": "LexBotの使い方ガイド",
        "howto_1": "1️⃣ 単語を登録する",
        "howto_1_desc": "- 📘または📚を選ぶと単語入力画面へ\n- 入力方法：✍️ 手動、📜 履歴",
        "howto_2": "2️⃣ クイズを作る（📘）",
        "howto_2_desc": "- 出題形式・言語ペアを選択\n- 翻訳／空欄補充、記述／選択式に対応",
        "howto_3": "3️⃣ フラッシュカードで暗記（📚）",
        "howto_3_desc": "- 表裏の切り替え・訳言語の変更が可能\n- 単語の削除やリセットも簡単！",
        "howto_4": "4️⃣ 学習履歴を見る（📜）",
        "howto_4_desc": "- 過去の結果・正誤が見られる\n- 間違えた単語だけ再学習もOK",
        "see_howto": "使い方ガイド",
        "welcome": "ようこそ",
        "login": "🔐 ログイン",
        "logged_in_as": "✅ ログイン中: ",
        "logout": "ログアウト",
        "email": "📧 メールアドレス",
        "password": "🔑 パスワード ",
        "login_with_email": "メールでログイン",
        "new_account_created": "新しいアカウントを作成しました: ",
        "login_failed": "ログイン失敗: ",
        "guest_mode": "ゲストモードで利用中。",
        "login_with_email": "メールでログイン",
        "logout": "ログアウト",
        "login_failed": "ログイン失敗: ",
        "make_new_account": "新規アカウント作成",
        "create_account": "アカウント作成",
        "account_created_successfully": " のアカウントを作成しました。",
        "account_creation_failed": "このアカウントは登録されています: ",
        "flashcard_all": "この単語でフラッシュカード",
        "flashcard_incorrect": "不正解のみでフラッシュカード",
        "no_vocab_warning": "クイズを始める前に単語を入力してください。",
        "history_title": "テスト履歴",
        "test": "テスト",
        "timestamp": "受験日",
        "questions": "問題一覧",
        "select_translation_language": "翻訳する言語を選択",
        "reset_success": "すべての単語がリセットされました",
        "deleted": "削除しました",
        "no_words_entered": "単語が入力されていません",
        "delete_word": "単語を削除"
    },
    "中文": {
        "title": "LexBot",
        "input_method": "请选择单词的输入方式",
        "manual": "手动输入",
        "camera": "从图像提取",
        "next": "下一步",
        "card_front": "正面",
        "card_back": "背面",
        "flip": "翻转",
        "next_card": "下一个",
        "back": "返回",
        "language_from": "你想学习的语言",
        "language_to": "您的语言",
        "image_toggle": "显示图片",
        "speak": "朗读",
        "Input by voice": "通过语音输入",
        "test_settings": "测试设置",
        "format": "形式",
        "context": "语境",
        "start_quiz": "开始测试",
        "input_words": "请输入单词（可使用空格或换行分隔多个）",
        "add_words": "添加",
        "current_words": "当前单词列表：",
        "to_config": "前往测试设置",
        "camera_title": "📷 使用相机读取单词",
        "extracted_words": "提取的单词：",
        "go_to_config": "前往测试设置",
        "show_image": "显示图片",
        "history": "历史记录",
        "no_history": "暂无历史记录。",
        "review_all": "重新进行本次测试",
        "review_wrong": "仅复习错误问题",
        "reset_all": "重置所有单词",
        "remove_card": "移除此卡片",
        "score": "得分",
        "your_answer": "你的回答",
        "correct_answer": "正确答案",
        "feedback": "反馈",
        "overall_feedback": "整体反馈",
        "start_over": "重新开始",
        "hint": "提示",
        "settings": "设置",
        "language_setting": "语言设置",
        "select_language": "选择界面语言",
        "selected_language": "当前选择的语言：",
        "apply": "应用",
        "cancel": "取消",
        "save": "保存",
        "close": "关闭",
        "notebook": "我的单词本",
        "no_words": "尚未添加任何单词。",
        "delete": "删除",
        "confirm_delete": "确定要删除这个单词吗？",
        "word_meaning": "含义",
        "synonyms": "同义词",
        "antonyms": "反义词",
        "part_of_speech": "词性",
        "example_sentence": "例句",
        "related_image": "相关图片",
        "created_at": "添加时间",
        "add_to_notebook": "添加到单词本",
        "flashcards": "抽认卡",
        "no_flashcards": "暂无抽认卡",
        "practice_mode": "练习模式",
        "quiz_mode": "测验模式",
        "show_answer": "显示答案",
        "hide_answer": "隐藏答案",
        "next_flashcard": "下一张卡片",
        "result_summary": "测试结果总结",
        "correct_count": "正确数量：",
        "wrong_count": "错误数量：",
        "review_summary": "复习总结",
        "delete_word": "删除单词",
        "history_description": "你以前的测验记录将显示在这里。",
        "redo_test": "重新进行完整测试",
        "redo_incorrect": "只复习错误的题目",
        "multiple-choice": "选择题",
        "written": "填空题",
        "language-translation": "翻译题",
        "fill-blank": "填空",
        "free-text": "简答题",
        "Voice input": "语音输入",
        "Input from camera": "来自相机的输入",
        "Input from history": "来自历史记录的输入",
        "enter_more_words": "继续输入单词",
        "clear_history": "清除历史记录",
        "no_history_yet": "暂无历史记录。",
        "howto_title": "LexBot 使用指南",
        "howto_1": "1️⃣ 添加单词",
        "howto_1_desc": "- 选择 📘 或 📚 进入单词输入界面\n- 输入方式：✍️ 手动、📜 历史记录",
        "howto_2": "2️⃣ 生成测验（📘）",
        "howto_2_desc": "- 选择题型和语言对\n- 支持翻译和填空题，书写或选择题",
        "howto_3": "3️⃣ 用闪卡记忆（📚）",
        "howto_3_desc": "- 可翻转卡片、选择翻译语言\n- 支持删除和重置单词",
        "howto_4": "4️⃣ 查看学习记录（📜）",
        "howto_4_desc": "- 查看过去的成绩与对错\n- 只重新学习错误的单词也可以",
        "see_howto": "使用指南",
        "welcome": "欢迎",
        "login": "🔐 登录",
        "logged_in_as": "✅ 已登录账户: ",
        "logout": "登出",
        "email": "📧 邮箱",
        "password": "🔑 密码",
        "login_with_email": "通过邮箱登录",
        "new_account_created": "已创建新账户: ",
        "login_failed": "登录失败: ",
        "guest_mode": "正在使用访客模式。",       
        "logout": "登出",
        "login_failed": "登录失败: ",
        "make_new_account": "创建新账户",
        "create_account": "创建账户",
        "account_created_successfully": " 账户创建成功。",
        "account_creation_failed": "此帐户已注册: ",
        "flashcard_all": "用所有单词制作抽认卡",
        "flashcard_incorrect": "用错误单词制作抽认卡",
        "no_vocab_warning": "请先输入一些单词再开始测验。",
        "history_title": "测试历史",
        "test": "测试",
        "timestamp": "考试日期",
        "questions": "题目列表",
        "select_translation_language": "选择翻译语言",
        "reset_success": "所有单词已重置",
        "deleted": "已删除",
        "no_words_entered": "未输入单词",
        "delete_word": "删除单词"
},
    "한국어": {
        "title": "LexBot",
        "input_method": "단어 입력 방법을 선택하세요",
        "manual": "직접 입력",
        "camera": "이미지에서 추출",
        "next": "다음",
        "card_front": "앞면",
        "card_back": "뒷면",
        "flip": "뒤집기",
        "next_card": "다음 카드",
        "back": "뒤로가기",
        "language_from": "배우고 싶은 언어",
        "language_to": "귀하의 언어",
        "image_toggle": "이미지 표시",
        "speak": "음성으로 듣기",
        "Input by voice": "음성으로 입력",
        "test_settings": "테스트 설정",
        "format": "형식",
        "context": "문맥",
        "start_quiz": "테스트 시작",
        "input_words": "단어 입력 (공백 또는 줄바꿈으로 여러 개 입력 가능)",
        "add_words": "추가",
        "current_words": "현재 단어 목록:",
        "to_config": "테스트 설정으로 이동",
        "camera_title": "📷 카메라로 단어 인식",
        "extracted_words": "추출된 단어:",
        "go_to_config": "테스트 설정으로 이동",
        "show_image": "이미지 표시",
        "history": "히스토리",
        "no_history": "히스토리가 없습니다.",
        "review_all": "이 단어 테스트 다시하기",
        "review_wrong": "틀린 문제만 다시하기",
        "reset_all": "모든 단어 초기화",
        "remove_card": "이 카드 삭제",
        "score": "점수",
        "your_answer": "당신의 답변",
        "correct_answer": "정답",
        "feedback": "피드백",
        "overall_feedback": "종합 피드백",
        "start_over": "처음부터 다시",
        "hint": "힌트",
        "settings": "설정",
        "language_setting": "언어 설정",
        "select_language": "인터페이스 언어 선택",
        "selected_language": "선택된 언어:",
        "apply": "적용",
        "cancel": "취소",
        "save": "저장",
        "close": "닫기",
        "notebook": "내 단어장",
        "no_words": "아직 단어가 없습니다.",
        "delete": "삭제",
        "confirm_delete": "이 단어를 삭제하시겠습니까?",
        "word_meaning": "의미",
        "synonyms": "유의어",
        "antonyms": "반의어",
        "part_of_speech": "품사",
        "example_sentence": "예문",
        "related_image": "관련 이미지",
        "created_at": "추가 날짜",
        "add_to_notebook": "단어장에 추가",
        "flashcards": "플래시카드",
        "no_flashcards": "플래시카드가 없습니다",
        "practice_mode": "연습 모드",
        "quiz_mode": "퀴즈 모드",
        "show_answer": "정답 보기",
        "hide_answer": "정답 숨기기",
        "next_flashcard": "다음 카드", 
        "result_summary": "테스트 결과 요약",
        "correct_count": "정답 수:",
        "wrong_count": "오답 수:",
        "review_summary": "복습 요약",
        "delete_word": "단어 삭제",
        "history_description": "이전에 시도한 테스트 기록이 여기에 표시됩니다.",
        "redo_test": "전체 테스트 다시 하기",
        "redo_incorrect": "틀린 문제만 복습하기",
        "multiple-choice": "객관식",
        "written": "주관식",
        "language-translation": "번역 문제",
        "fill-blank": "빈칸 채우기",
        "free-text": "주관식",
        "Voice input": "음성 입력",
        "Input from camera": "카메라에서 입력",
        "Input from history": "기록에서 입력",
        "enter_more_words": "단어 더 입력하기",
        "clear_history": "히스토리 삭제",
        "no_history_yet": "히스토리가 없습니다.",
        "howto_title": "LexBot 사용 가이드",
        "howto_1": "1️⃣ 단어 등록하기",
        "howto_1_desc": "- 📘 또는 📚 버튼을 눌러 단어 입력 화면으로 이동\n- 입력 방법: ✍️ 수동, 📜 기록",
        "howto_2": "2️⃣ 퀴즈 만들기 (📘)",
        "howto_2_desc": "- 문제 형식과 언어 쌍 선택\n- 번역/빈칸 문제, 서술형/객관식 모두 지원",
        "howto_3": "3️⃣ 플래시카드로 암기하기 (📚)",
        "howto_3_desc": "- 카드 앞뒤 전환 및 번역 언어 설정 가능\n- 단어 삭제/초기화도 간편",
        "howto_4": "4️⃣ 학습 기록 확인하기 (📜)",
        "howto_4_desc": "- 이전 결과와 정오표 확인 가능\n- 틀린 단어만 다시 학습할 수도 있어요",
        "see_howto": "사용 가이드",
        "welcome": "환영합니다",
        "login": "🔐 로그인",
        "logged_in_as": "✅ 로그인됨: ",
        "logout": "로그아웃",
        "email": "📧 이메일",
        "password": "🔑 비밀번호",
        "login_with_email": "이메일로 로그인",
        "new_account_created": "새 계정 생성됨: ",
        "login_failed": "로그인 실패: ",
        "guest_mode": "게스트 모드 사용 중.",
        "login_with_email": "이메일로 로그인",
        "logout": "로그아웃",
        "login_failed": "로그인 실패: ",
        "make_new_account": "새 계정 만들기",
        "create_account": "계정 생성",
        "account_created_successfully": " 계정이 성공적으로 생성되었습니다.",
        "account_creation_failed": "이 계정이 등록되었습니다: ",
        "flashcard_all": "모든 단어로 플래시카드",
        "flashcard_incorrect": "오답 단어로 플래시카드",
        "no_vocab_warning": "퀴즈를 시작하기 전에 단어를 입력해주세요.",
        "history_title": "테스트 기록",
        "test": "테스트",
        "timestamp": "응시 날짜",
        "questions": "문제 목록",
        "select_translation_language": "번역 언어를 선택하세요",
        "reset_success": "모든 단어가 초기화되었습니다",
        "deleted": "삭제됨",
        "no_words_entered": "단어가 입력되지 않았습니다",
        "delete_word": "단어 삭제"
    },
    "Español": {
        "title": "LexBot",
        "input_method": "Seleccione el método de entrada de palabras",
        "manual": "Entrada manual",
        "camera": "Extraer desde imagen",
        "next": "Siguiente",
        "card_front": "Anverso",
        "card_back": "Reverso",
        "flip": "Voltear",
        "next_card": "Siguiente tarjeta",
        "back": "Atrás",
        "language_from": "Idioma que quieres aprender",
        "language_to": "Tu idioma",
        "image_toggle": "Mostrar imagen",
        "speak": "Leer en voz alta",
        "Input by voice": "Entrada por voz",
        "test_settings": "Configuración de prueba",
        "format": "Formato",
        "context": "Contexto",
        "start_quiz": "Iniciar prueba",
        "input_words": "Introduzca palabras (separadas por espacio o salto de línea)",
        "add_words": "Añadir",
        "current_words": "Lista actual de palabras:",
        "to_config": "Ir a configuración de prueba",
        "camera_title": "📷 Leer palabras con la cámara",
        "extracted_words": "Palabras extraídas:",
        "go_to_config": "Ir a configuración de prueba",
        "show_image": "Mostrar imagen",
        "history": "Historial",
        "no_history": "No hay historial todavía.",
        "review_all": "Repetir esta prueba",
        "review_wrong": "Repetir solo los errores",
        "reset_all": "Restablecer todas las palabras",
        "remove_card": "Eliminar esta tarjeta",
        "score": "Puntuación",
        "your_answer": "Tu respuesta",
        "correct_answer": "Respuesta correcta",
        "feedback": "Comentario",
        "overall_feedback": "Comentario general",
        "start_over": "Comenzar de nuevo",
        "hint": "Pista",
        "settings": "Configuración",
        "language_setting": "Configuración de idioma",
        "select_language": "Seleccionar idioma de la interfaz",
        "selected_language": "Idioma seleccionado:",
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "save": "Guardar",
        "close": "Cerrar",
        "notebook": "Mi cuaderno de palabras",
        "no_words": "No hay palabras todavía.",
        "delete": "Eliminar",
        "confirm_delete": "¿Está seguro de que desea eliminar esta palabra?",
        "word_meaning": "Significado",
        "synonyms": "Sinónimos",
        "antonyms": "Antónimos",
        "part_of_speech": "Categoría gramatical",
        "example_sentence": "Frase de ejemplo",
        "related_image": "Imagen relacionada",
        "created_at": "Añadido en",
        "add_to_notebook": "Agregar al cuaderno",
        "flashcards": "Tarjetas de memoria",
        "no_flashcards": "No hay tarjetas disponibles",
        "practice_mode": "Modo práctica",
        "quiz_mode": "Modo prueba",
        "show_answer": "Mostrar respuesta",
        "hide_answer": "Ocultar respuesta",
        "next_flashcard": "Siguiente tarjeta",
        "result_summary": "Resumen de resultados",
        "correct_count": "Respuestas correctas:",
        "wrong_count": "Respuestas incorrectas:",
        "review_summary": "Resumen de repaso",
        "delete_word": "Eliminar palabra",
        "history_description": "Tus intentos anteriores de prueba se mostrarán aquí.",
        "redo_test": "Rehacer prueba completa",
        "redo_incorrect": "Revisar solo las respuestas incorrectas",
        "multiple-choice": "Elección múltiple",
        "written": "Respuesta escrita",
        "language-translation": "Traducción",
        "fill-blank": "Completar espacio en blanco",
        "free-text": "Respuesta libre",
        "Voice input": "Entrada por voz",
        "Input from camera": "Entrada desde la cámara",
        "Input from history": "Entrada desde el historial",
        "enter_more_words": "Agregar más palabras",
        "clear_history": "Borrar historial",
        "no_history_yet": "No hay historial todavía.",
        "howto_title": "Guía de uso de LexBot",
        "howto_1": "1️⃣ Añadir vocabulario",
        "howto_1_desc": "- Elige 📘 o 📚 para ingresar palabras\n- Métodos de entrada: ✍️ Manual, 📜 Historial",
        "howto_2": "2️⃣ Crear un cuestionario (📘)",
        "howto_2_desc": "- Selecciona formato y par de idiomas\n- Compatible con traducción, completar espacios, opción múltiple o texto libre",
        "howto_3": "3️⃣ Estudiar con tarjetas (📚)",
        "howto_3_desc": "- Voltea tarjetas y elige el idioma de traducción\n- Puedes eliminar o reiniciar palabras fácilmente",
        "howto_4": "4️⃣ Ver historial de aprendizaje (📜)",
        "howto_4_desc": "- Consulta tus resultados anteriores y errores\n- Repite sólo las palabras incorrectas si lo deseas",
        "see_howto": "Guía de uso",
        "welcome": "Bienvenido",
        "login": "🔐 Iniciar sesión",
        "logged_in_as": "✅ Sesión iniciada como: ",
        "logout": "Cerrar sesión",
        "email": "📧 Correo electrónico",
        "password": "🔑 Contraseña",
        "login_with_email": "Iniciar sesión con correo",
        "new_account_created": "Nueva cuenta creada: ",
        "login_failed": "Error al iniciar sesión: ",
        "guest_mode": "Modo invitado activo.",
        "new_account_created": "Nueva cuenta creada: ",
        "make_new_account": "Crear nueva cuenta",
        "create_account": "Crear cuenta",
        "account_created_successfully": " cuenta creada con éxito.",
        "account_creation_failed": "Esta cuenta está registrada: ",
        "flashcard_all": "Tarjetas con todas las palabras",
        "flashcard_incorrect": "Tarjetas con errores",
        "no_vocab_warning": "Por favor, ingrese algunas palabras antes de comenzar la prueba.",
        "history_title": "Historial de pruebas",
        "test": "Prueba",
        "timestamp": "Fecha",
        "questions": "Preguntas",
        "select_translation_language": "Seleccione el idioma de traducción",
        "reset_success": "Todas las palabras han sido restablecidas",
        "deleted": "Eliminado",
        "no_words_entered": "No se han ingresado palabras",
        "delete_word": "Eliminar palabra"
    },
}

T = ui_text[st.session_state.ui_lang]

# ==== 2. セッション初期化 ====
if 'stage' not in st.session_state:
    st.session_state.stage = 'select-input'

for key, default in {
    'vocab': [], 'quiz': [], 'answers': [], 'history': [],
    'flashcard_index': 0, 'current_flashcard': [], 'flipped': False,
    'translation_direction': 'en-to-ja'
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if "deleted_words" not in st.session_state:
    st.session_state.deleted_words = []

if 'stage' not in st.session_state:
    st.session_state.stage = 'select-input'
    
if 'page_stack' not in st.session_state:
    st.session_state.page_stack = []
    
if "ui_lang" not in st.session_state:
    st.session_state.ui_lang = "en"  # または "ja" など、デフォルト言語
    
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    
if "is_guest" not in st.session_state:
    st.session_state.is_guest = False

# ==== 3. ユーティリティ関数群 ====
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Voice input in progress... Please speak")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='en-EN')
        return text
    except:
        st.warning("Voice recognition failed")
        return ""

def safe_generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted as e:
        st.error("❗ You have reached your free usage limit for Gemini. Please wait until tomorrow or consider a paid plan.")
        st.stop()

def grade_quiz(quiz, answers):
    prompt = f"""
Please grade the quiz:
Quiz: {json.dumps(quiz)}
Answers: {json.dumps(answers)}
Output format:
{{"scorePercentage": number, "incorrect": [{{"question": string, "yourAnswer": string, "yourAnswerMeaning": string, "correctAnswer": string, "correctMeaning": string, "feedback": string}}], "overallFeedback": string}}
    """
    response = model.generate_content(prompt)
    cleaned = re.sub(r"^```json|```$", "", response.text.strip(), flags=re.MULTILINE).strip()

    return json.loads(cleaned)

def save_history():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": now,
        "vocab": st.session_state.vocab,
        "quiz": st.session_state.quiz,
        "answers": st.session_state.answers
    }
    st.session_state.history.append(entry)
    
def generate_flashcards(vocab, direction):
    cards = []
    for word in vocab:
        if direction == "en-to-ja":
            cards.append({"front": word, "back": f"Meaning of {word}"})
        else:
            cards.append({"front": f"Meaning of {word}", "back": word})
    return cards

def render_language_selector(key="ui_lang_selector"):
    current_lang = st.session_state.get("ui_lang", "English")
    selected = st.selectbox("🗣 " + ui_text[current_lang]["language_setting"], LANGUAGES, index=LANGUAGES.index(current_lang), key=key)
    if selected != current_lang:
        st.session_state.ui_lang = selected
        st.rerun()        

def grade_dummy(quiz, answers):
    # 絶対に辞書を返すように明示
    return {
        "scorePercentage": 80,
        "correct": [...],
        "incorrect": [...],
        "overallFeedback": "Nice"
    }

# 2. 画面遷移は必ずこの関数を使う
def change_stage(new_stage):
    # 現在の画面を履歴に追加（重複防止）
    if st.session_state.stage != new_stage:
        st.session_state.page_stack.append(st.session_state.stage)
    st.session_state.stage = new_stage
    
def show_history_screen():
    T = ui_text[st.session_state.ui_lang]

    st.markdown(f"### 📜 {T['history_title']}")

    if "history" not in st.session_state or not st.session_state.history:
        st.info(T["no_history_yet"])
    else:
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{T['test']} {len(st.session_state.history) - i}"):
                st.markdown(f"- {T['score']}: {entry['score']}")
                st.markdown(f"- {T['timestamp']}: {entry['timestamp']}")
                st.markdown("#### 📋 " + T["questions"])
                for j, q in enumerate(entry["quiz"]):
                    st.markdown(f"**{j+1}. {q['question']}**")
                    if "choices" in q:
                        for choice in q["choices"]:
                            st.markdown(f"- {choice}")
                    st.markdown(f"*{T['your_answer']}:* {entry['answers'][j]}")
                    st.markdown(f"*{T['correct_answer']}:* {q['answer']}")
                    st.markdown("---")

    # ✅ 修正済：戻るボタン（page_stackに input_words が入っている場合にも対応）
    if st.button("🔙 " + T["back"], key="back_button_in_history"):
        if st.session_state.get("page_stack"):
            dest = st.session_state.page_stack.pop()
            if dest == "input_words":
                st.session_state.stage = "input"  # ← input_words は input に変換
            else:
                st.session_state.stage = dest
            st.rerun()
        else:
            st.warning(T["no_history"])

# ==== サイドバー ====
def render_sidebar():
    T = ui_text.get(st.session_state.get("ui_lang", "English"), {})

    with st.sidebar:
        st.markdown("## Menu")

        if st.button("📘 " + T["start_quiz"]):
            st.session_state.input_mode = "test"
            change_stage("input")
            st.session_state.next_stage = "config"

        if st.button("📚 " + T["flashcards"]):
            st.session_state.input_mode = "flashcard"
            change_stage("input")
            st.session_state.next_stage = "flashcard"

        if st.button("📜 " + T["history"]):
            change_stage("history")

        render_language_selector("ui_lang_sidebar")

# ==== Main Menu Screen ====
def main_menu():
    T = ui_text[st.session_state.ui_lang]
    
    st.markdown(
    f"<h1 style='text-align:center; font-size:48px; color:#4CAF50;'>{T['welcome']}</h1>", 
    unsafe_allow_html=True
)
            
    if st.button(f"🔍 {T['see_howto']}"):
        st.session_state.stage = "howto"
        st.rerun()
            
def howto_guide():
    T = ui_text[st.session_state.ui_lang]
    st.title(T["howto_title"])
    st.markdown(f"### {T['howto_1']}")
    st.markdown(T["howto_1_desc"])
    st.markdown(f"### {T['howto_2']}")
    st.markdown(T["howto_2_desc"])
    st.markdown(f"### {T['howto_3']}")
    st.markdown(T["howto_3_desc"])
    st.markdown(f"### {T['howto_4']}")
    st.markdown(T["howto_4_desc"])

    if st.button("🔙 " + T["back"], key="back_button_in_howto_guide"):
        st.session_state.stage = "select-input"
        st.rerun()
        
if "stage" not in st.session_state:
    st.session_state.stage = "main_menu"

if st.session_state.stage == "main_menu":
    main_menu()
elif st.session_state.stage == "howto":
    howto_guide()
    
# ==== Word Input Screen ====
def input_words():
    T = ui_text[st.session_state.ui_lang]
    st.title("📥 " + T["input_words"])

    vocab = st.session_state.get("vocab", [])
    updated_vocab = vocab.copy()
    delete_index = None  # Index to delete

    for i, word in enumerate(vocab):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i+1}. {word}")
        with col2:
            if st.button("❌", key=f"delete_{word}_{i}"):
                delete_index = i

    if delete_index is not None:
        removed_word = updated_vocab.pop(delete_index)
        st.session_state.vocab = updated_vocab
        st.success(f"{T['delete']} '{removed_word}'")
        st.rerun()

    option = st.radio(T["input_method"], (
        T["manual"], T["Input from history"]))

    # 単語追加と自動遷移処理
    def handle_word_addition(words):
        now = datetime.now()
        if "wordbook" not in st.session_state:
            st.session_state.wordbook = []
        for word in words:
            st.session_state.wordbook.append({"word": word, "added_at": now})

        if "vocab" not in st.session_state:
            st.session_state.vocab = []
        st.session_state.vocab += words

        st.success(T["add_words"])
        if st.session_state.get("input_mode") == "test":
            st.session_state.stage = "config"
        elif st.session_state.get("input_mode") == "flashcard":
            st.session_state.stage = "flashcard"

        st.rerun()

    if option == T["manual"]:
        text = st.text_area(T["input_words"])
        if st.button(T["add_words"]):
            words = [w.strip().lower() for w in text.split() if w.isalpha()]
            handle_word_addition(words)

    if "temp_extracted_words" not in st.session_state:
        st.session_state.temp_extracted_words = []

    elif option == T["Input from history"]:
        st.session_state.page_stack = st.session_state.get("page_stack", [])
        st.session_state.page_stack.append("input_words")
        st.session_state.stage = "history"
        st.rerun()

    # 抽出語が存在すれば表示し、追加ボタンを表示
    if st.session_state.temp_extracted_words:
        st.markdown(f"### 🔍 {T['extracted_words']}")
        st.write(st.session_state.temp_extracted_words)
        if st.button("✅ " + T["add_words"]):
            handle_word_addition(st.session_state.temp_extracted_words)
            st.session_state.temp_extracted_words = []
            
    if st.button("🔙 " + T["back"], key="back_button_in_input_words"):
        if st.session_state.get("page_stack"):
            st.session_state.stage = st.session_state.page_stack.pop()
            st.rerun()
        else:
            st.warning(T["no_history"])
            
# ===== クイズ生成 =====
CODE_TO_LANG_LABELS = {
    "en": "English",
    "ja": "日本語",
    "zh": "中文",
    "ko": "한국어",
    "es": "Español",
}

QUIZ_EXAMPLES = {
    "multiple-choice": {
        "language-translation": {
            "en-ja": [
                {"question": "What is the Japanese translation of 'nature'?", "options": ["科学", "自然", "法律", "動物"], "correctAnswer": "自然"}
            ],
            "en-zh": [
                {"question": "What is the Chinese translation of 'nature'?", "options": ["科技", "自然", "法律", "动物"], "correctAnswer": "自然"}
            ],
            "en-ko": [
                {"question": "What is the Korean translation of 'nature'?", "options": ["과학", "자연", "법률", "동물"], "correctAnswer": "자연"}
            ],
            "en-es": [
                {"question": "What is the Spanish translation of 'nature'?", "options": ["ciencia", "naturaleza", "ley", "animal"], "correctAnswer": "naturaleza"}
            ],
            "ja-en": [
                {"question": "「水」は英語で？", "options": ["wine", "rain", "water", "snow"], "correctAnswer": "water"}
            ],
            "ja-zh": [
                {"question": "「水」は中国語で？", "options": ["火", "水", "风", "山"], "correctAnswer": "水"}
            ],
            "ja-ko": [
                {"question": "「水」は韓国語で？", "options": ["불", "바람", "물", "땅"], "correctAnswer": "물"}
            ],
            "ja-es": [
                {"question": "「水」はスペイン語で？", "options": ["fuego", "aire", "agua", "tierra"], "correctAnswer": "agua"}
            ],
            "zh-en": [
                {"question": "“快乐” 的英文是？", "options": ["happy", "lucky", "fast", "smart"], "correctAnswer": "happy"}
            ],
            "zh-ja": [
                {"question": "“水”的日文是？", "options": ["火", "水", "風", "山"], "correctAnswer": "水"}
            ],
            "zh-ko": [
                {"question": "“水”的韓文は？", "options": ["불", "바람", "물", "땅"], "correctAnswer": "물"}
            ],
            "zh-es": [
                {"question": "“水”的西班牙语是？", "options": ["fuego", "aire", "agua", "tierra"], "correctAnswer": "agua"}
            ],
            "ko-en": [
                {"question": "“고양이”는 영어로 무엇입니까?", "options": ["dog", "cat", "bird", "cow"], "correctAnswer": "cat"}
            ],
            "ko-ja": [
                {"question": "“고양이”는 일본어로 무엇입니까?", "options": ["犬", "猫", "鳥", "馬"], "correctAnswer": "猫"}
            ],
            "ko-zh": [
                {"question": "“고양이”는 중국어로 무엇입니까?", "options": ["狗", "猫", "鸟", "马"], "correctAnswer": "猫"}
            ],
            "ko-es": [
                {"question": "“고양이”는 스페인어로 무엇입니까?", "options": ["perro", "gato", "ave", "pez"], "correctAnswer": "gato"}
            ],  
            "es-en": [
                {"question": "¿Cómo se dice “sol” en inglés?", "options": ["moon", "sun", "star", "sky"], "correctAnswer": "sun"}
            ],
            "es-ja": [
                {"question": "¿Cómo se dice “sol” en japonés?", "options": ["月", "空", "星", "太陽"], "correctAnswer": "太陽"}
            ],
            "es-zh": [
                {"question": "¿Cómo se dice “sol” en chino?", "options": ["月亮", "太阳", "星星", "天气"], "correctAnswer": "太阳"}
            ],
            "es-ko": [
                {"question": "¿Cómo se dice “sol” en coreano？", "options": ["달", "별", "태양", "하늘"], "correctAnswer": "태양"}
            ]
        },
        "fill-blank": {
            "en": [
                {"question": "This unusual weather pattern is considered a natural __________.", "options": ["policy", "phenomenon", "strategy", "mechanism"], "correctAnswer": "phenomenon"}
            ],
            "ja": [
                {"question": "彼の行動はとても__________で、誰も予想できなかった。", "options": ["平凡", "独特", "論理的", "安定"], "correctAnswer": "独特"}
            ],
            "zh": [
                {"question": "他提出的这个想法非常__________，值得深入研究。", "options": ["传统", "独特", "简单", "普通"], "correctAnswer": "独特"}
            ],
            "ko": [
                {"question": "그의 발표는 매우 __________ 내용으로 모두의 주목을 받았다.", "options": ["평범한", "독창적인", "지루한", "무의미한"], "correctAnswer": "독창적인"}
            ],
            "es": [
                {"question": "Este descubrimiento científico es un gran __________ en la medicina moderna.", "options": ["error", "paso", "avance", "problema"], "correctAnswer": "avance"}
            ]
        }
    },
    "free-text": {
        "language-translation": {
            "en-ja": [
                {"question": "What is the Japanese word for 'river'?", "correctAnswer": "川／かわ"}
            ],
            "en-zh": [
                {"question": "What is the Chinese word for 'river'?", "correctAnswer": "河流／河"}
            ],
            "en-ko": [
                {"question": "What is the Korean word for 'river'?", "correctAnswer": "강"}
            ],
            "en-es": [
                {"question": "What is the Spanish word for 'river'?", "correctAnswer": "río"}
            ],
            "ja-en": [
                {"question": "「りんご」は英語で？", "correctAnswer": "apple"}
            ],
            "ja-zh": [
                {"question": "「りんご」は中国語で？", "correctAnswer": "苹果"}
            ],
            "ja-ko": [
                {"question": "「りんご」は韓国語で？", "correctAnswer": "사과"}
            ],
            "ja-es": [
                {"question": "「りんご」はスペイン語で？", "correctAnswer": "manzana"}
            ],
            "zh-en": [
                {"question": "“朋友” 的英文是？", "correctAnswer": "friend"}
            ],
            "zh-ja": [
                {"question": "“朋友” 的日文は？", "correctAnswer": "友達／ともだち"}
            ],
            "zh-ko": [
                {"question": "“朋友” 的韩文は？", "correctAnswer": "친구"}
            ],
            "zh-es": [
                {"question": "“朋友” 的西班牙文は？", "correctAnswer": "amigo"}
            ],
            "ko-en": [
                {"question": "“학교”는 영어로 무엇입니까?", "correctAnswer": "school"}
            ],
            "ko-ja": [
                {"question": "“학교”는 일본어로 무엇입니까?", "correctAnswer": "学校／がっこう"}
            ],
            "ko-zh": [
                {"question": "“학교”는 중국어로 무엇입니까?", "correctAnswer": "学校"}
            ],
            "ko-es": [
                {"question": "“학교”는 스페인어로 무엇입니까?", "correctAnswer": "escuela"}
            ],
            "es-en": [
                {"question": "¿Cómo se dice “cielo” en inglés?", "correctAnswer": "sky"}
            ],
            "es-ja": [
                {"question": "¿Cómo se dice “cielo” en japonés?", "correctAnswer": "空／そら"}
            ],
            "es-zh": [
                {"question": "¿Cómo se dice “cielo” en chino?", "correctAnswer": "天空／天"}
            ],
            "es-ko": [
                {"question": "¿Cómo se dice “cielo” en coreano？", "correctAnswer": "하늘"}
            ]
        },
        "fill-blank": {
            "en": [
                {"question": "This unusual weather pattern is considered a natural __________.", "correctAnswer": "phenomenon"}
            ],
            "ja": [
                {"question": "彼の__________は誰にとっても衝撃的だった。", "correctAnswer": "発言"}
            ],
            "zh": [
                {"question": "他每天早上都会喝一杯__________来开始一天的生活。", "correctAnswer": "咖啡"}
            ],
            "ko": [
                {"question": "그는 항상 약속 시간에 __________ 도착한다.", "correctAnswer": "늦게"}
            ],
            "es": [
                {"question": "Ella siempre lleva un __________ cuando hace frío.", "correctAnswer": "abrigo"}
            ]
        }
    }
}
def generate_quiz(words, format, context, count):
    direction = st.session_state.get("translation_direction", "en-to-ja")
    from_code, to_code = direction.split("-to-")

    from_lang_label = CODE_TO_LANG_LABELS.get(from_code, from_code)
    to_lang_label = CODE_TO_LANG_LABELS.get(to_code, to_code)

    example_list = QUIZ_EXAMPLES.get(format, {}).get(context, {}).get(f"{from_code}-{to_code}", [])
    if not example_list:
        example_list = []

    example_json = json.dumps(example_list, ensure_ascii=False, indent=2)

    translation_instruction = f"""
Using the following words, create {count} {context} questions in the {format} format.
Language pair: {from_lang_label} → {to_lang_label}
Use real words in the options (not a, b, c). Ensure natural context and appropriate difficulty.
Make sure each quiz item includes both "question" and "correctAnswer" keys.
Randomize the order of the words when generating questions.
For multiple-choice questions, randomize the order of the answer options.
Create the questions in a way that helps the learner understand and remember the meaning and usage of each word.
Return the output as a pure JSON array starting with [] (no explanations or markdown)
    """

    prompt = f"""
単語リスト: {', '.join(words)}
問題数: {count}

{translation_instruction}

出力形式（JSONリスト）例:
{example_json}
    """

    return prompt


# ===== 採点 =====
def grade(quiz, answers):
    ui_lang_code = LANG_CODES.get(st.session_state.get("ui_lang", "English"), "en")
    lang_label = CODE_TO_LANG_LABELS.get(ui_lang_code, "English")

    prompt = f"""
Please grade the following quiz and answers, and output the results in {lang_label}.
All feedback and messages should be written in natural {lang_label}.

Also, generate quizzes that help learners reinforce the vocabulary they got wrong.

Quiz: {json.dumps(quiz, ensure_ascii=False)}
Answers: {json.dumps(answers, ensure_ascii=False)}

Output format (JSON):
{{
  "scorePercentage": number (e.g., 80),
  "incorrect": [
    {{
      "question": string,
      "yourAnswer": string,
      "yourAnswerMeaning": string,
      "correctAnswer": string,
      "correctMeaning": string,
      "feedback": string
    }}
  ],
  "overallFeedback": string
}}

* Output must be a plain JSON object (starting with {{), no markdown, no explanation.
"""

    response = model.generate_content(prompt)
    cleaned = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE).strip()

    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
        else:
            st.error("❌ Unexpected data format. The response is not a valid JSON object.")
            return {
                "scorePercentage": 0,
                "incorrect": [],
                "overallFeedback": "Grading failed."
            }
    except Exception as e:
        st.error(f"❌ JSON parsing error: {e}")
        st.text_area("Response content (for debugging)", value=cleaned, height=300)
        return {
            "scorePercentage": 0,
            "incorrect": [],
            "overallFeedback": "Grading failed."
        }

# ==== 翻訳方向設定 ====
if st.session_state.stage == 'config':
    T = ui_text[st.session_state.ui_lang]
    st.subheader(T["test_settings"])

    # UI上の表示（多言語対応）
    format_ui = st.selectbox(T["format"], [T["multiple-choice"], T["written"]])
    context_ui = st.selectbox(T["context"], [T["language-translation"], T["fill-blank"]])

    # 表示→コード（英語）へのマッピング
    FORMAT_LABELS = {
        T["multiple-choice"]: "multiple-choice",
        T["written"]: "free-text"
    }
    CONTEXT_LABELS = {
        T["language-translation"]: "language-translation",
        T["fill-blank"]: "fill-blank"
    }

    format = FORMAT_LABELS.get(format_ui, "multiple-choice")
    context = CONTEXT_LABELS.get(context_ui, "language-translation")

    if context == "language-translation":
        from_lang = st.selectbox(T["language_from"], LANGUAGES, key="from_lang")
        to_langs = [l for l in LANGUAGES if l != from_lang]
        to_lang = st.selectbox(T["language_to"], to_langs, key="to_lang")
        st.session_state.translation_direction = f"{LANG_CODES[from_lang]}-to-{LANG_CODES[to_lang]}"

    vocab_count = len(st.session_state.vocab)
    
    if vocab_count == 0:
        st.warning(T["no_vocab_warning"])
        count = 0
    else:
        count = st.number_input(
            T["start_quiz"],
            min_value=1,
            max_value=vocab_count,
            value=vocab_count,
            key="quiz_count_input"
    )

    if st.button(T["start_quiz"], key="start_quiz"):
        prompt = generate_quiz(st.session_state.vocab, format, context, int(count))
        quiz_json_str = model.generate_content(prompt).text
        st.code(quiz_json_str, language="json")

        try:
            cleaned_str = re.sub(r"^```json|```$", "", quiz_json_str.strip(), flags=re.MULTILINE).strip()
            quiz_data = json.loads(cleaned_str)

            for idx, item in enumerate(quiz_data):
                if "question" not in item:
                    if "correctAnswer" in item:
                        vocab_word = st.session_state.vocab[idx] if idx < len(st.session_state.vocab) else "word"
                        item["question"] = f"{T['your_answer']}: '{vocab_word}'"
                    else:
                        st.error(f"❌ Question {idx+1} is missing the 'question' field. Possible Gemini response error.")
                        st.stop()

            st.session_state.quiz = quiz_data
            st.session_state.stage = "quiz"
            st.session_state.format = format
            st.rerun()

        except json.JSONDecodeError:
            st.error("❌ Failed to parse quiz JSON. Gemini response format may be invalid.")
            st.stop()

    if st.button("🔙 " + T["back"], key="back_button_in_config"):
        if st.session_state.get("page_stack"):
            st.session_state.stage = st.session_state.page_stack.pop()
            st.rerun()
        else:
            st.warning(T["no_history"])

# ==== クイズ画面 ====
elif st.session_state.stage == 'quiz':
    T = ui_text[st.session_state.ui_lang] 
    st.subheader("📝 " + T["start_quiz"])
    answers = []
    for i, q in enumerate(st.session_state.quiz):
        question_text = q.get("question", "(No question text)")
        st.write(f"{T['hint']} {i+1}: {question_text}")
        if st.session_state.format == 'multiple-choice':
            ans = st.radio(T["your_answer"], q['options'], key=f"q_{i}")
        else:
            ans = st.text_input(T["your_answer"], key=f"q_{i}")
            if 'hint' in q and st.button(f"{T['hint']} {i+1}", key=f"hint_{i}"):
                st.write(T["hint"] + ":", q['hint'])
        answers.append({"answer": ans})

    if st.button(T["score"], key="grade_quiz"):
        st.session_state.answers = answers
        st.session_state.stage = 'results'
        st.rerun()

# ==== 結果画面 ====
elif st.session_state.stage == 'results':
    T = ui_text[st.session_state.ui_lang]  

    if 'result' not in st.session_state or st.session_state.result is None:
        try:
            result = grade(st.session_state.quiz, st.session_state.answers)  # ← 修正: grade_quiz → grade
            st.session_state.result = result
            save_history()
        except Exception as e:
            st.error(f"❌ The marking failed: {e}")
            st.stop()
    else:
        result = st.session_state.result

    st.subheader("📊 " + T["result_summary"])
    
    if isinstance(result, dict) and "scorePercentage" in result:
        st.write(f"{T['score']}: {result['scorePercentage']}%")
    else:
        st.error("❌ The result data format is invalid.")
        st.write("Contents of debug result:", result)
        st.stop()

    incorrect_words = []

    for i, item in enumerate(result.get("incorrect", [])):
        st.write(f"{T['hint']} {i+1}: {item['question']}")
        st.write(f"- {T['your_answer']}: {item['yourAnswer']} → {item['yourAnswerMeaning']}")
        st.write(f"- {T['correct_answer']}: {item['correctAnswer']} → {item['correctMeaning']}")
        st.write(f"- {T['feedback']}: {item['feedback']}")
        incorrect_words.append(item['correctAnswer'])

    st.write(T["overall_feedback"] + ":")
    st.write(result["overallFeedback"])

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔁 " + T["start_over"], key="restart"):
            for key in ['stage', 'vocab', 'quiz', 'answers', 'current_flashcard', 'flashcard_index', 'flipped', 'result']:
                st.session_state[key] = [] if isinstance(st.session_state.get(key), list) else 0 if isinstance(st.session_state.get(key), int) else False if isinstance(st.session_state.get(key), bool) else 'select-input'
            st.rerun()

    with col2:
        if st.button("📘 " + T["review_all"], key="redo_all_words"):
            st.session_state.stage = 'config'
            st.session_state.result = None
            st.rerun()

    with col3:
        if incorrect_words and st.button("❌ " + T["review_wrong"], key="redo_incorrect_only"):
            st.session_state.vocab = incorrect_words
            st.session_state.stage = 'config'
            st.session_state.result = None
            st.rerun()

# ==== フラッシュカード表示 ====
LANG_OPTIONS = {
    "English": "en",
    "日本語": "ja",
    "中文": "zh",
    "한국어": "ko",
    "Español": "es",
}

MULTI_LANG_TRANSLATIONS = {
    "apple": {"ja": "りんご", "zh": "苹果", "ko": "사과", "es": "manzana"},
    "山": {"en": "mountain", "zh": "山", "ko": "산", "es": "montaña"},
    "朋友": {"en": "friend", "ja": "友達", "ko": "親友", "es": "amigo"},
    "学校": {"en": "school", "zh": "学校", "ko": "학교", "es": "escuela"},
    "sol": {"en": "sun", "ja": "太陽", "zh": "太阳", "ko": "태양"},
}

def generate_multilang_flashcards(words, source_lang):
    cards = []
    for word in words:
        card = {"front": word}
        translations = MULTI_LANG_TRANSLATIONS.get(word, {})
        for label, code in LANG_OPTIONS.items():
            card[f"back_{code}"] = translations.get(code, "---")
        cards.append(card)
    return cards

# ==== Gemini翻訳 ====
def translate_with_gemini(word, target_lang_code):
    cache_key = f"{word}_{target_lang_code}"
    if cache_key in st.session_state.translation_cache:
        return st.session_state.translation_cache[cache_key]

    prompt = f"Translate the word '{word}' into the language code '{target_lang_code}'. Only return the translated word."
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        st.session_state.translation_cache[cache_key] = result
        print(f"🔄 Gemini Translation: {word} → {target_lang_code} = {result}")
        return result
    except Exception as e:
        print("❌ Gemini translation failure:", e)
        return "---"

# ==== セッション初期化 ====
for key in [
    "translation_language", "vocab", "previous_vocab", "current_flashcard",
    "flashcard_index", "flipped", "translation_cache"
]:
    if key not in st.session_state:
        if key in ["vocab", "previous_vocab", "current_flashcard"]:
            st.session_state[key] = []
        elif key == "translation_language":
            st.session_state[key] = "English"
        elif key == "flashcard_index":
            st.session_state[key] = 0
        elif key == "flipped":
            st.session_state[key] = False
        elif key == "translation_cache":
            st.session_state[key] = {}

# ==== フラッシュカード画面 ====
if st.session_state.stage == 'flashcard':
    T = ui_text[st.session_state.ui_lang] 
    st.subheader(f"📚 {T['flashcards']}")

    st.session_state.translation_language = st.selectbox(
        T["select_translation_language"],
        LANG_OPTIONS.keys(),
        index=list(LANG_OPTIONS.keys()).index(st.session_state.translation_language)
    )

    current_words = st.session_state.get("vocab", [])

    if st.session_state.previous_vocab != current_words and current_words:
        st.session_state.previous_vocab = current_words.copy()
        st.session_state.current_flashcard = generate_multilang_flashcards(current_words, source_lang="en")
        st.session_state.flashcard_index = 0
        st.session_state.flipped = False

    cards = st.session_state.current_flashcard

    if not cards:
        st.info(T["no_words_entered"])
    else:
        index = st.session_state.flashcard_index % len(cards)
        card = cards[index]
        lang_code = LANG_OPTIONS[st.session_state.translation_language]

        if st.session_state.flipped:
            side = f'back_{lang_code}'
            if not card.get(side) or card[side] == "---":
                translated = translate_with_gemini(card['front'], lang_code)
                card[side] = translated or "---"
            content = card[side]
        else:
            content = card['front']

        st.markdown(f"""
<div style='
    border: 3px solid #4CAF50;
    padding: 24px;
    border-radius: 16px;
    background-color: #ccffcc;
    font-size: 48px;
    text-align: center;
    margin: 20px 0;
    color: black;
    min-height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
'>
    <strong>{content}</strong>
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🔄 {T['flip']}", key="flip_flashcard"):
                st.session_state.flipped = not st.session_state.flipped
                st.rerun()
        with col2:
            if st.button(f"➡ {T['next']}", key="next_flashcard"):
                st.session_state.flashcard_index = (st.session_state.flashcard_index + 1) % len(cards)
                st.session_state.flipped = False
                st.rerun()

        if st.button(f"🚫 {T['reset_all']}"):
            st.session_state.vocab = []
            st.session_state.previous_vocab = []
            st.session_state.current_flashcard = []
            st.session_state.flashcard_index = 0
            st.session_state.flipped = False
            st.session_state.translation_cache = {}
            st.success(T["reset_success"])
            st.rerun()

        if st.button(f"🗑 {T['delete_word']}"):
            removed_word = card['front']
            st.session_state.vocab = [w for w in st.session_state.vocab if w != removed_word]
            st.session_state.previous_vocab = st.session_state.vocab.copy()
            st.session_state.current_flashcard = generate_multilang_flashcards(
                st.session_state.vocab, source_lang="en"
            )
            st.session_state.flashcard_index = 0
            st.session_state.flipped = False
            st.success(f"{T['deleted']}「{removed_word}」")
            st.rerun()

    if st.button(f"🔙 {T['enter_more_words']}", key="back_from_flashcard"):
        st.session_state.stage = 'input'
        st.rerun()

# ==== 履歴表示 ====
def show_history_screen():
    import hashlib
    T = ui_text[st.session_state.ui_lang]
    st.subheader(f"🕓 {T['history']}")
    st.write(T["history_description"])

    if not st.session_state.history:
        st.info(T["no_history_yet"])

    # === 重複除去: タイムスタンプ + 語彙 のハッシュで重複判定 ===
    unique_entries = []
    seen_hashes = set()
    for entry in reversed(st.session_state.history):
        sorted_vocab = sorted(entry.get('vocab', []))  # 並び順を正規化
        hash_input = entry['timestamp'] + ",".join(sorted_vocab)
        h = hashlib.md5(hash_input.encode()).hexdigest()
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique_entries.append(entry)

    # === 表示 ===
    for i, h in enumerate(unique_entries):
        timestamp = h.get('timestamp', 'N/A')
        vocab_list = h.get('vocab', [])
        quiz_list = h.get('quiz', [])
        answer_list = h.get('answers', [])

        # 正答カウント
        correct_count = 0
        vocab_display = []
        for word, q, a in zip(vocab_list, quiz_list, answer_list):
            user_answer = a.get('answer', '').strip().lower()
            correct_answer = q.get('correctAnswer', '').strip().lower()
            if user_answer and correct_answer and user_answer == correct_answer:
                correct_count += 1
                vocab_display.append(f"{word} ✓")
            else:
                vocab_display.append(f"{word} ✗")

        # 正答率（ゼロ除算防止）
        total = len(quiz_list)
        score = int((correct_count / total) * 100) if total else 0

        st.markdown(f"### 📅 {timestamp}")
        st.markdown(f"#### {' '.join(vocab_display)}　{score}%")

        incorrect_vocab = [
            word for word, q, a in zip(vocab_list, quiz_list, answer_list)
            if a.get('answer', '').strip().lower() != q.get('correctAnswer', '').strip().lower()
        ]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button(f"{T['redo_test']} (#{len(unique_entries)-i})", key=f"redo_all_{i}"):
                st.session_state.vocab = vocab_list
                st.session_state.stage = 'config'
                st.rerun()
        with col2:
            if incorrect_vocab:
                if st.button(f"{T['redo_incorrect']} (#{len(unique_entries)-i})", key=f"redo_incorrect_{i}"):
                    st.session_state.vocab = incorrect_vocab
                    st.session_state.stage = 'config'
                    st.rerun()
        with col3:
            if st.button(f"{T['flashcard_all']}", key=f"flashcard_{i}"):
                st.session_state.vocab = vocab_list
                st.session_state.stage = 'flashcard'
                st.rerun()

        with col4:
            if incorrect_vocab:
                if st.button(f"{T['flashcard_incorrect']}", key=f"flashcard_incorrect_{i}"):
                    st.session_state.vocab = incorrect_vocab
                    st.session_state.stage = 'flashcard'
                    st.rerun()

    # 履歴全消去
    if st.button(T["clear_history"], key="clear_history"):
        st.session_state.history = []
        st.rerun()

# ==== Gemini fallbackエラーハンドリング ====
from google.api_core.exceptions import ResourceExhausted

def safe_generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted as e:
        st.error(T["gemini_limit_error"])
        st.stop()

# ==== 6. 画面ルーティング ====
render_sidebar()
if st.session_state.stage == 'select-input':
    main_menu()
elif st.session_state.stage == 'input':
    input_words()
elif st.session_state.stage == 'config':
    # ★ テスト設定画面をこのまま残すか、必要に応じて関数化してもOK
    st.subheader("Test Setup")
    # 以下略（すでに上に実装済みなのでそれを活かす）
elif st.session_state.stage == 'quiz':
    # ★ ここもクイズ画面の本体コードに置き換える
    st.subheader("Test")
    # すでにあるクイズ処理コードをここに入れるか、関数化して呼び出す
elif st.session_state.stage == 'results':
    # ★ 結果画面
    st.subheader("result")
    # 採点表示ややり直し機能をここで呼ぶ
elif st.session_state.stage == 'flashcard':
    # ✅ すでに表示コードあり → 何もしなくてOK（コード本体がすでにある）
    pass
elif st.session_state.stage == 'history':
    show_history_screen()  # ← 関数にしてあるのでこれでOK




