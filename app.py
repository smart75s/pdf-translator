import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
from PIL import Image
import io

# --- الإعدادات ---
# تأكد من وضع مفتاح الـ API الخاص بك هنا
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="المترجم الذكي المطور", page_icon="🚀")

st.title("🚀 المترجم الاحترافي (النسخة المستقرة)")
st.info("جاهز لترجمة ملفات الـ Scan والنصوص بدقة عالية.")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة"):
        with st.spinner("جاري التواصل مع عقل Gemini وتحليل الصفحات..."):
            try:
                # استخدام الموديل بشكل مباشر وتجنب مشاكل الإصدارات
                model = genai.GenerativeModel('gemini-1.5-flash')

                # قراءة محتوى الملف
                file_bytes = uploaded_file.read()
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                full_result = ""

                # معالجة أول 3 صفحات (لضمان عمل التطبيق بسرعة في البداية)
                num_pages = min(len(doc), 3)
                
                for i in range(num_pages):
                    page = doc[i]
                    # تحويل الصفحة لصورة ليراها Gemini بدقة
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    # طلب الترجمة من Gemini
                    prompt = "Identify the language of this document and translate all its content to Arabic. If it is already in Arabic, translate it to English. Output ONLY the translated text."
                    response = model.generate_content([prompt, img])
                    
                    full_result += f"\n--- الصفحة {i+1} ---\n{response.text}\n"

                if full_result:
                    st.success("تمت الترجمة بنجاح!")
                    st.text_area("النص المترجم:", full_result, height=400)
                    st.download_button("📥 تحميل النتيجة (txt)", full_result.encode('utf-8'), file_name="translated_file.txt")
                else:
                    st.error("لم يتمكن النظام من استخراج نص من الملف.")

            except Exception as e:
                st.error(f"حدث خطأ فني: {str(e)}")
                st.info("نصيحة: تأكد من صحة مفتاح API وتوافر حصة مجانية في حسابك.")
