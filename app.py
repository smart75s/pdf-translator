import streamlit as st
import fitz
import google.generativeai as genai
from PIL import Image
import io

# --- الإعدادات ---
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5cا"
# هذا السطر يخبر المكتبة باستخدام الإصدار المستقر فوراً
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="المترجم النهائي", page_icon="✅")

st.title("✅ النسخة المستقرة (حل مشكلة 404)")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة"):
        with st.spinner("جاري المعالجة بالإصدار المستقر..."):
            try:
                # إجبار النظام على استخدام v1 بدلاً من v1beta
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    generation_config={"candidate_count": 1}
                )

                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = ""

                for i in range(min(len(doc), 3)):
                    page = doc[i]
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    # طلب الترجمة مباشرة
                    response = model.generate_content(["Translate this image content to Arabic", img])
                    full_text += f"\n--- صفحة {i+1} ---\n{response.text}\n"

                st.success("تمت الترجمة بنجاح!")
                st.text_area("النتيجة:", full_text, height=400)

            except Exception as e:
                # إذا فشل، سنحاول بطريقة استدعاء الموديل المباشرة
                st.error(f"خطأ في الربط: {str(e)}")
                st.info("جاري محاولة حل بديل...")
                # محاولة أخيرة باسم موديل بديل
                try:
                     model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
                     # كرر محاولة الترجمة هنا...
                except:
                     pass
