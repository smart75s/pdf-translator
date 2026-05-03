import streamlit as st
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator

st.set_page_config(page_title="مترجم الـ PDF الاحترافي", page_icon="📄")

st.title("📄 مترجم ملفات PDF الذكي")

# إعدادات اللغة
col1, col2 = st.columns(2)
with col1:
    source_l = st.selectbox("لغة الملف الأصلية:", ["ar", "en", "fr"])
with col2:
    target_l = st.selectbox("الترجمة إلى:", ["en", "ar", "fr"])

uploaded_file = st.file_uploader("ارفع ملف PDF هنا", type="pdf")

if uploaded_file:
    if st.button("بدء المعالجة والترجمة"):
        with st.spinner("جاري استخراج النصوص والترجمة..."):
            try:
                # فتح الملف
                file_bytes = uploaded_file.read()
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                
                full_translated_text = ""
                extracted_pages = 0

                for page in doc:
                    # استخراج النص الخام
                    raw_text = page.get_text().strip()
                    
                    if raw_text:
                        # إذا وجد نص، نقوم بترجمته
                        try:
                            translated = GoogleTranslator(source=source_l, target=target_l).translate(raw_text)
                            full_translated_text += f"\n--- صفحة {page.number + 1} ---\n{translated}\n"
                            extracted_pages += 1
                        except Exception as e:
                            st.warning(f"فشلت ترجمة الصفحة {page.number + 1}")
                    
                if full_translated_text:
                    st.success(f"تمت ترجمة {extracted_pages} صفحة بنجاح!")
                    st.text_area("النص المترجم:", full_translated_text, height=300)
                    
                    st.download_button(
                        label="📥 تحميل ملف الترجمة",
                        data=full_translated_text.encode('utf-8'),
                        file_name="translated_result.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("⚠️ لم يتم العثور على نصوص قابلة للقراءة في هذا الملف. قد يكون الملف عبارة عن صور (Scan).")
                    st.info("نصيحة: جرب رفع ملف PDF يحتوي على نصوص يمكنك تحديدها ونسخها بالماوس.")

            except Exception as e:
                st.error(f"حدث خطأ فني: {str(e)}")
