import streamlit as st
import fitz
import requests
import base64
import io
from PIL import Image

# --- الإعدادات ---
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"
# استخدام الإصدار المستقر v1 لحل مشكلة 404
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="المترجم الذكي", page_icon="🎯")
st.title("🎯 المترجم الاحترافي (الإصدار المستقر)")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة"):
        with st.spinner("جاري التواصل مع سيرفرات جوجل المستقرة..."):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_byte_arr = io.BytesIO()
                Image.open(io.BytesIO(pix.tobytes("png"))).save(img_byte_arr, format='PNG')
                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Translate the content of this image to Arabic accurately."},
                            {"inline_data": {"mime_type": "image/png", "data": img_base64}}
                        ]
                    }]
                }
                
                response = requests.post(URL, json=payload)
                res_json = response.json()

                if response.status_code == 200:
                    translated = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("تمت الترجمة بنجاح!")
                    st.write(translated)
                else:
                    st.error(f"خطأ {response.status_code}: جوجل تقول أن هذا المسار غير متاح.")
                    st.json(res_json)

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
