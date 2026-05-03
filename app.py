import streamlit as st
import fitz
import requests
import base64
import io
from PIL import Image

# --- الإعدادات ---
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="المترجم الذكي", page_icon="🛡️")
st.title("🛡️ مترجم الطوارئ (نسخة التشخيص)")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة"):
        with st.spinner("جاري فحص الاتصال وترجمة الصفحة الأولى..."):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                
                # نأخذ الصفحة الأولى فقط للاختبار
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_byte_arr = io.BytesIO()
                Image.open(io.BytesIO(pix.tobytes("png"))).save(img_byte_arr, format='PNG')
                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Translate the following image to Arabic."},
                            {"inline_data": {"mime_type": "image/png", "data": img_base64}}
                        ]
                    }]
                }
                
                response = requests.post(URL, json=payload)
                res_json = response.json()

                # فحص الرد للتأكد من عدم وجود أخطاء من جوجل
                if response.status_code != 200:
                    st.error(f"خطأ من سيرفر جوجل ({response.status_code})")
                    st.json(res_json) # سيعرض لنا السبب الحقيقي للرفض
                elif 'candidates' not in res_json:
                    st.warning("جوجل استلمت الطلب ولكنها لم ترسل ترجمة. السبب محتمل:")
                    st.write(res_json.get('promptFeedback', 'قيود على المحتوى أو المفتاح'))
                else:
                    translated = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("تمت ترجمة الصفحة الأولى بنجاح!")
                    st.write(translated)

            except Exception as e:
                st.error(f"حدث خطأ غير متوقع: {str(e)}")
