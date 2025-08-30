
import streamlit as st
from openai import OpenAI
import uuid

st.set_page_config(page_title="App Conselhos Amorosos 💕", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def chat_response(prompt, system_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"

def traduzir_texto(texto, idioma_destino="PT"):
    try:
        prompt = f"Traduz o seguinte texto para {idioma_destino} mantendo o mesmo significado e tom:\n\n{texto}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception:
        return texto

idioma = st.selectbox("Escolhe o idioma 🌐", options=["PT", "EN", "ES", "FR", "DE"])
st.title(traduzir_texto("💘 Conselhos Amorosos com IA", idioma))

tab1, tab2, tab3, tab4 = st.tabs([
    traduzir_texto("Conselhos", idioma),
    traduzir_texto("Respostas", idioma),
    traduzir_texto("Alma gêmea", idioma),
    traduzir_texto("Filhos", idioma)
])

# Tab 1
with tab1:
    st.subheader(traduzir_texto("Fala comigo sobre os teus sentimentos ❤️", idioma))
    if "chat1" not in st.session_state:
        st.session_state.chat1 = []
    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input := st.chat_input(traduzir_texto("Partilha o que sentes...", idioma)):
        st.session_state.chat1.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        response = chat_response(
            user_input,
            traduzir_texto("És um terapeuta empático que dá conselhos amorosos com humanidade.", idioma)
        )
        response_trad = traduzir_texto(response, idioma)
        st.session_state.chat1.append({"role": "assistant", "content": response_trad})
        with st.chat_message("assistant"):
            st.markdown(response_trad)

# Tab 2
with tab2:
    st.subheader(traduzir_texto("Mostra a mensagem e vamos ajudar 📩", idioma))
    if "chat2" not in st.session_state:
        st.session_state.chat2 = []
    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if user_input2 := st.chat_input(traduzir_texto("Cola aqui a mensagem que recebeste...", idioma)):
        st.session_state.chat2.append({"role": "user", "content": user_input2})
        with st.chat_message("user"):
            st.markdown(user_input2)
        response2 = chat_response(
            user_input2,
            traduzir_texto("És um especialista em comunicação amorosa. Ajuda a criar uma resposta empática, romântica e natural.", idioma)
        )
        response2_trad = traduzir_texto(response2, idioma)
        st.session_state.chat2.append({"role": "assistant", "content": response2_trad})
        with st.chat_message("assistant"):
            st.markdown(response2_trad)

# Tab 3
with tab3:
    st.subheader(traduzir_texto("Descobre quem é a tua alma gêmea 💞", idioma))
    if "chat3" not in st.session_state:
        st.session_state.chat3 = []
    if user_input3 := st.chat_input(traduzir_texto("Fala-me sobre a pessoa que te interessa...", idioma)):
        st.session_state.chat3.append({"role": "user", "content": user_input3})
        response3 = chat_response(
            user_input3,
            traduzir_texto("És um especialista em compatibilidade amorosa. Analisa e descreve a alma gêmea do usuário.", idioma)
        )
        response3_trad = traduzir_texto(response3, idioma)
        st.session_state.chat3.append({"role": "assistant", "content": response3_trad})
        st.markdown(response3_trad)

# Tab 4
with tab4:
    st.subheader(traduzir_texto("Descobre como serão os teus filhos 👶", idioma))
    if "chat4" not in st.session_state:
        st.session_state.chat4 = []
    if user_input4 := st.chat_input(traduzir_texto("Conta-me sobre ti e a outra pessoa...", idioma)):
        st.session_state.chat4.append({"role": "user", "content": user_input4})
        response4 = chat_response(
            user_input4,
            traduzir_texto("És um especialista em família e genética amorosa. Descreve como seriam os filhos do casal.", idioma)
        )
        response4_trad = traduzir_texto(response4, idioma)
        st.session_state.chat4.append({"role": "assistant", "content": response4_trad})
        st.markdown(response4_trad)
