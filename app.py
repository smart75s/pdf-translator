import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import io
from PIL import Image

# --- إعداد Gemini ---
# ضع مفتاحك هنا أو الأفضل استخدامه كـ Secret في Streamlit
API_KEY = "AIzaSyBKDOw4XIXMSu18WI-H6lOQEoLkjEe6X5c" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

st.set_page_config(page_title="مترجم الـ PDF بالذكاء الاصطناعي", page_icon="🤖")

st.title("🤖 مترجم الـ PDF الذكي (يدعم الصور والـ Scan)")
st.write("هذه النسخة تستخدم Gemini لقراءة وترجمة أي نوع من الملفات.")

uploaded_file = st.file_uploader("ارفع ملف PDF (نصي أو صورة)", type="pdf")

if uploaded_file:
    if st.button("بدء الترجمة الاحترافية"):
        with st.spinner("جاري تحليل الصفحات وترجمتها بواسطة Gemini..."):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                final_output = ""

                # معالجة أول 5 صفحات (للحفاظ على السرعة)
                for i in range(min(len(doc), 5)):
                    page = doc[i]
                    
                    # تحويل الصفحة لصورة ليراها Gemini (حل مشكلة الـ Scan)
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    # إرسال الصورة لـ Gemini مع أمر الترجمة
                    prompt = "Extract all text from this image and translate it to Arabic. If it's already Arabic, translate it to English. Provide only the translation."
                    response = model.generate_content([prompt, img])
                    
                    final_output += f"\n--- الصفحة {i+1} ---\n{response.text}\n"

                st.success("تمت الترجمة بنجاح!")
                st.text_area("النتيجة:", final_output, height=400)
                
                st.download_button("تحميل الترجمة", final_output.encode('utf-8'), file_name="gemini_translation.txt")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
