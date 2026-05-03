import streamlit as st
import fitz
import requests
import base64
import io
from PIL import Image

# --- الإعدادات ---
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"

st.set_page_config(page_title="المترجم الذكي المطور", page_icon="🎯")
st.title("🎯 مترجم الطوارئ الذكي")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة"):
        with st.spinner("جاري البحث عن أفضل موديل متاح للترجمة..."):
            try:
                # 1. تحضير الملف
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_byte_arr = io.BytesIO()
                Image.open(io.BytesIO(pix.tobytes("png"))).save(img_byte_arr, format='PNG')
                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Translate this image to Arabic accurately."},
                            {"inline_data": {"mime_type": "image/png", "data": img_base64}}
                        ]
                    }]
                }

                # 2. قائمة الموديلات (هنا توضع القائمة)
                models_to_try = [
                    "gemini-1.5-pro",
                    "gemini-1.5-flash",
                    "gemini-1.0-pro-vision-latest"
                ]

                success = False
                for model_name in models_to_try:
                    # محاولة الاتصال بكل موديل حتى ينجح واحد
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        translated = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"✅ تم بنجاح باستخدام موديل: {model_name}")
                        st.write(translated)
                        success = True
                        break # توقف عن البحث فور النجاح
                    else:
                        st.warning(f"⚠️ الموديل {model_name} غير متاح في منطقتك حالياً.")

                if not success:
                    st.error("❌ للأسف، جميع الموديلات المتاحة لم تستجب. تأكد من صلاحية مفتاح الـ API.")

            except Exception as e:
                st.error(f"حدث خطأ غير متوقع: {str(e)}")
