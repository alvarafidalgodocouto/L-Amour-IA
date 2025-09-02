import streamlit as st

st.set_page_config(page_title="💘 Love Advice AI", layout="wide")

st.title("💘 Love Advice AI")
st.markdown("Choose one of our **4 services** to get started:")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_love_advice.py", label="💌 Love Advice Chat")
    st.page_link("pages/2_message_replies.py", label="💬 Message Reply Suggestions")

with col2:
    st.page_link("pages/3_soulmate.py", label="✨ Discover Your Soulmate")
    st.page_link("pages/4_children.py", label="👶 Visualize Your Children")
