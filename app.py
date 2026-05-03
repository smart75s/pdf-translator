import streamlit as st

st.title("مرحباً بك!")
st.write("إذا كنت ترى هذه الرسالة، فهذا يعني أن التطبيق يعمل بنجاح.")

# اختبار رفع ملف بسيط
file = st.file_uploader("جرب رفع ملف هنا")
if file:
    st.success("تم رفع الملف بنجاح!")
