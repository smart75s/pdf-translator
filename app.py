import streamlit as st
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator

# 1. إعدادات الصفحة
st.set_page_config(page_title="مترجم الـ PDF", page_icon="📄")

# 2. تنسيق الواجهة (بسيط وخفيف)
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div.stButton > button { width: 100%; background-color: #2e7d32; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 مترجم ملفات PDF")
st.write("ترجم ملفاتك فوراً بين العربية والإنجليزية.")

# 3. خيارات اللغة
col1, col2 = st.columns(2)
with col1:
    source_l = st.selectbox("لغة الملف:", ["ar", "en"])
with col2:
    target_l = st.selectbox("ترجم إلى:", ["en", "ar"])

# 4. رفع الملف
uploaded_file = st.file_uploader("اختر ملف PDF", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة"):
        with st.spinner("جاري معالجة الملف والترجمة..."):
            try:
                # فتح الـ PDF
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                final_text = ""
                
                # ترجمة أول 5 صفحات فقط كمرحلة أولى لضمان السرعة
                num_pages = min(len(doc), 10) 
                
                for i in range(num_pages):
                    page_text = doc[i].get_text()
                    if page_text.strip():
                        translated = GoogleTranslator(source=source_l, target=target_l).translate(page_text)
                        final_text += f"\n--- الصفحة {i+1} ---\n{translated}\n"
                
                st.success("تمت الترجمة بنجاح!")
                st.text_area("النص المترجم:", final_text, height=300)
                
                st.download_button("تحميل النص المترجم", final_text, file_name="translated.txt")
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
