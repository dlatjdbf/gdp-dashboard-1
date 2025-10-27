import streamlit as st
import base64
import requests
import json

st.title("AI 카페인 분석기 ☕")

uploaded_file = st.file_uploader("음식 또는 음료 사진을 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="업로드한 이미지", use_container_width=True)

    # 이미지를 base64로 변환
    img_bytes = uploaded_file.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # OpenAI API 호출
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer YOUR_OPENAI_API_KEY"}
    payload = {
        "model": "gpt-4o-mini",  # gpt-5-vision-preview 대신 접근 가능한 모델로 교체 가능
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 사진 속 음식 또는 음료의 종류를 인식하고 카페인 함유 여부와 예상 함량을 알려줘."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_base64}"}
                ]
            }
        ]
    }

    with st.spinner("AI가 분석 중입니다..."):
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()

    # 오류 확인
    if "choices" in result_json:
        result = result_json["choices"][0]["message"]["content"]
        st.success("AI 분석 결과")
        st.write(result)
    else:
        st.error("⚠️ API 응답 오류 발생. 아래 JSON을 확인하세요.")
        st.json(result_json)
