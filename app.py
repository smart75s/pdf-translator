import streamlit as st
import fitz
import requests
import base64
import io
from PIL import Image

# --- الإعدادات ---
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="المترجم السريع", page_icon="⚡")
st.title("⚡ المترجم المباشر (تجاوز التعليق)")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة الفورية"):
        with st.spinner("جاري الترجمة عبر الرابط المباشر..."):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = ""

                # معالجة أول صفحتين للتأكد من السرعة
                for i in range(min(len(doc), 2)):
                    page = doc[i]
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                    img_byte_arr = io.BytesIO()
                    Image.open(io.BytesIO(pix.tobytes("png"))).save(img_byte_arr, format='PNG')
                    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

                    # إنشاء الطلب المباشر لجوجل
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": "Translate this image to Arabic accurately."},
                                {"inline_data": {"mime_type": "image/png", "data": img_base64}}
                            ]
                        }]
                    }
                    
                    response = requests.post(URL, json=payload)
                    result = response.json()
                    
                    # استخراج النص من الرد
                    translated_text = result['candidates'][0]['content']['parts'][0]['text']
                    full_text += f"\n--- صفحة {i+1} ---\n{translated_text}\n"

                st.success("تمت الترجمة بنجاح!")
                st.text_area("النتيجة:", full_text, height=400)

            except Exception as e:
                st.error(f"فشل الاتصال المباشر: {str(e)}")
                st.info("تأكد من أن مفتاح الـ API صحيح ومفعل.")
