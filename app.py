import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
from PIL import Image
import io

# --- الإعدادات ---
# تأكد من وضع مفتاح الـ API الخاص بك هنا بشكل صحيح
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="المترجم الذكي المطور", page_icon="🚀")

st.title("🚀 المترجم الخارق (النسخة المستقرة)")
st.info("تم إصلاح أخطاء التنسيق والربط. جاهز للعمل!")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF (نصي أو Scan)", type="pdf")

if uploaded_file:
    if st.button("إطلاق الترجمة"):
        with st.spinner("جاري التواصل مع عقل Gemini..."):
            try:
                # محاولة الوصول للموديل بالتسمية المستقرة
                model = genai.GenerativeModel('gemini-1.5-flash')

                # قراءة الملف المرفوع
                file_content = uploaded_file.read()
                doc = fitz.open(stream=file_content, filetype="pdf")
                full_text = ""

                # ترجمة أول 3 صفحات لضمان السرعة
                pages_to_translate = min(len(doc), 3)
                
                for i in range(pages_to_translate):
                    page = doc[i]
                    # تحويل الصفحة لصورة بجودة عالية
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    # طلب الترجمة
                    prompt = "Translate the text in this image to Arabic accurately. Maintain the context."
                    response = model.generate_content([prompt, img])
                    
                    full_text += f"\n--- صفحة {i+1} ---\n{response.text}\n"

                if full_text:
                    st.success("تمت الترجمة بنجاح!")
                    st.text_area("النص الناتج:", full_text, height=400)
                    st.download_button("تحميل الترجمة", full_text.encode('utf-8'), file_name="translated.txt")
                else:
                    st.warning("لم يتم استخراج أي نص.")

            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء المعالجة: {str(e)}")
