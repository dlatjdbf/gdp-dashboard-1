import streamlit as st
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="AI 카페인 분석기 ☕", layout="centered")
st.title("🤖 AI 카페인 분석기 (무료 인공지능 버전)")

st.markdown("""
이 AI는 **MobileNetV2 딥러닝 모델**을 기반으로 작동합니다.  
사진을 업로드하면 음식의 종류를 예측하고,  
카페인 함유 가능성을 알려줍니다.
""")

# -------------------------------
# 카페인 데이터베이스
# -------------------------------
CAFFEINE_DB = {
    "coffee": 120,
    "espresso": 150,
    "latte": 90,
    "tea": 25,
    "green_tea": 30,
    "cola": 34,
    "chocolate": 9,
    "energy_drink": 80,
    "matcha": 70,
    "americano": 95,
    "black_tea": 45
}

# -------------------------------
# 모델 불러오기
# -------------------------------
@st.cache_resource
def load_model():
    model = MobileNetV2(weights="imagenet")
    return model

model = load_model()

# -------------------------------
# 업로드 이미지 입력
# -------------------------------
uploaded_file = st.file_uploader("📸 음식 또는 음료 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="업로드한 이미지", use_container_width=True)

    # 이미지 전처리
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # -------------------------------
    # AI 예측 수행
    # -------------------------------
    with st.spinner("AI가 이미지를 분석 중입니다... 🔍"):
        preds = model.predict(x)
        decoded = decode_predictions(preds, top=3)[0]

    st.subheader("🔍 AI 예측 결과 (상위 3개)")
    for i, (id_, label, prob) in enumerate(decoded):
        st.write(f"{i+1}. {label} — {prob*100:.2f}%")

    # -------------------------------
    # 카페인 예측 로직
    # -------------------------------
    predicted_label = decoded[0][1].lower()
    caffeine_value = None
    matched_key = None

    for key in CAFFEINE_DB:
        if key in predicted_label:
            caffeine_value = CAFFEINE_DB[key]
            matched_key = key
            break

    st.markdown("---")
    if caffeine_value:
        st.success(f"☕ **{matched_key.capitalize()}** 로 인식되었습니다. 예상 카페인 함량은 약 **{caffeine_value}mg** 입니다.")
    else:
        st.info("💧 카페인이 포함되지 않은 음식일 가능성이 높습니다.")
else:
    st.info("사진을 업로드하면 AI가 자동으로 분석합니다 ☕")
