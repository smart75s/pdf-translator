import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
from PIL import Image
import io

# --- الإعدادات ---
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="المترجم الذكي المطور", page_icon="🚀")

st.title("🚀 المترجم الخارق (نسخة الحل النهائي)")
st.info("هذه النسخة مصممة لتجاوز أخطاء الربط والتعرف على الصور.")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF (نصي أو Scan)", type="pdf")

if uploaded_file:
    if st.button("إطلاق الترجمة"):
        with st.spinner("جاري التواصل مع عقل Gemini..."):
            try:
                # محاولة الوصول للموديل بأكثر من تسمية لضمان العمل
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                except:
                    model = genai.GenerativeModel('models/gemini-1.5-flash')

                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = ""

                # معالجة أول 3 صفحات كاختبار قوة
                for i in range(min(len(doc), 3)):
                    page = doc[i]
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # تحسين جودة الصورة
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    # طلب الترجمة بوضوح
                    prompt = "Translate the text in this image to Arabic accurately. Maintain the context."
                    response = model.generate_content([prompt, img])
                    
                    full_text += f"\n--- صفحة {i+1} ---\n{response.text}\n"

                st.success("تم الاتصال والترجمة بنجاح!")
                st.text_area("النص الناتج:", full_text, height=400)

            
              except Exception as e:
                st.error(f"عذراً، لا يزال هناك تعارض: {str(e)}")
                st.info("تأكد أن مفتاح الـ API يعمل بشكل صحيح في Google AI Studio.")
