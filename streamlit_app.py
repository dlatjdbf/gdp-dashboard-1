import streamlit as st
import requests
import base64
import json

uploaded_file = st.file_uploader("음식 또는 음료 사진을 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="업로드한 이미지", use_container_width=True)
    img_bytes = uploaded_file.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # ✅ 안전한 방식으로 API 키 불러오기
    headers = {"Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"}

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",  # 이미지 입력 지원 모델
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 사진 속 음식 또는 음료의 종류를 인식하고, 카페인 함유 여부와 예상 함량을 알려줘."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_base64}"}
                ]
            }
        ]
    }

    with st.spinner("AI가 분석 중입니다..."):
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()

    if "choices" in result_json:
        st.success("AI 분석 결과")
        st.write(result_json["choices"][0]["message"]["content"])
    else:
        st.error("API 오류 발생")
        st.json(result_json)

