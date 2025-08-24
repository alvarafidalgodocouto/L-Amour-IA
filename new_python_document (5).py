
import os
import streamlit as st
from PIL import Image, ImageOps
import io
import openai
from datetime import datetime


st.set_page_config(page_title="💘 Conselhos Amorosos — UX Melhorado", layout="wide")
st.markdown("""
<style>
/* cores e estilo */
.block-title { font-size:22px; color:#6b2a57; font-weight:600; }
.stButton>button { background:#ff6b81; color:white; border-radius:10px; padding:8px 14px; }
.sidebar .stSelectbox { color:#6b2a57; }
.app-container { background: linear-gradient(180deg,#fff6fb,#fff); padding:10px; border-radius:12px; }
.card { background: #fff; border-radius:12px; padding:14px; box-shadow: 0 6px 18px rgba(0,0,0,0.06); }
small.help { color:#666; }
</style>
""", unsafe_allow_html=True)


OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY
    USE_OPENAI = True
else:
    USE_OPENAI = False


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


if "chat_conselhos" not in st.session_state:
    st.session_state.chat_conselhos = [] 
if "chat_respostas" not in st.session_state:
    st.session_state.chat_respostas = []
if "alma_form" not in st.session_state:
    st.session_state.alma_form = {}
if "alerts" not in st.session_state:
    st.session_state.alerts = []

def call_openai_chat(system_prompt: str, history: list, user_message: str, temperature: float = 0.7):
    """
    history: list of {"role":"user"|"assistant","text":...} previous turns (will be appended to system_prompt)
    """
    if not USE_OPENAI:
        
        if "conselho" in system_prompt.lower():
            return "Sinto isso contigo — tenta comunicar com honestidade e um passo pequeno (ex.: propor um café). Cuida de ti primeiro."
        else:
            
            return "Resposta exemplo: 'Adorei a tua mensagem — conta-me mais? 😊'"
    try:
        messages = [{"role": "system", "content": system_prompt}]
        for turn in history:
            role = "user" if turn["role"] == "user" else "assistant"
            messages.append({"role": role, "content": turn["text"]})
        messages.append({"role": "user", "content": user_message})
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=600
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Erro ao contactar API de IA: {e}")
        return "Desculpa, agora não consigo gerar a resposta (erro na API)."


SYSTEM_PROMPT_CONSELHOS = (
    "You are an empathetic, professional relationship coach. "
    "Respond with compassion, human warmth, and practical steps. "
    "Keep the response concise (3-6 sentences) and include 1-3 actionable suggestions. "
    "Do not moralize. Ask one gentle clarifying question if needed."
)

SYSTEM_PROMPT_RESPOSTAS = (
    "You are a message assistant that writes short, natural replies to received messages. "
    "Given a message from another person, provide exactly three reply options labeled "
    "'Gentle', 'Confident', and 'Playful'. Each reply must be 1-2 sentences, copy-ready, and friendly."
)


with st.sidebar:
    st.markdown("<div class='block-title'>💘 Conselhos Amorosos</div>", unsafe_allow_html=True)
    st.markdown("Escolhe idioma (apenas UI):")
    lang = st.selectbox("", ["pt", "en"], index=0)
    st.markdown("---")
    st.markdown("**Chave OpenAI:**")
    if USE_OPENAI:
        st.success("OpenAI key detectada — chats com qualidade GPT ativos.")
    else:
        st.warning("Sem OpenAI key — a app corre em modo demo (respostas simplificadas).")
    st.markdown("---")
    st.markdown("**Privacidade:** Envia selfies só se concordares que serão processadas temporariamente para gerar a imagem. Não armazenamos por defeito.")

tab1_label = "Precisas de um bom conselho para a tua relação?"
tab2_label = "Não sabes o que responder? Cola a mensagem aqui que te ajudamos!"
tab3_label = "Descobre quem é a tua alma gêmea"
tab4_label = "👶 Descobre como serão os teus filhos (opcional)"

tabs = st.tabs([tab1_label, tab2_label, tab3_label, tab4_label])


with tabs[0]:
    st.markdown("### 💬 " + tab1_label)
    st.write("Escreve livremente sobre a tua relação — a IA responde com empatia e passos práticos.")
    
    for turn in st.session_state.chat_conselhos:
        if turn["role"] == "user":
            st.chat_message("user").markdown(turn["text"])
        else:
            st.chat_message("assistant").markdown(turn["text"])

    prompt = st.chat_input("Partilha a tua situação ou pergunta aqui...")
    if prompt:
        
        st.session_state.chat_conselhos.append({"role": "user", "text": prompt})
        st.chat_message("user").markdown(prompt)

        
        answer = call_openai_chat(SYSTEM_PROMPT_CONSELHOS, st.session_state.chat_conselhos, prompt, temperature=0.7)
        st.session_state.chat_conselhos.append({"role": "assistant", "text": answer})
        st.chat_message("assistant").markdown(answer)


with tabs[1]:
    st.markdown("### 💬 " + tab2_label)
    st.write("Cole aqui a mensagem recebida e a IA dá 3 respostas prontas para usar.")
    
    for turn in st.session_state.chat_respostas:
        if turn["role"] == "user":
            st.chat_message("user").markdown(turn["text"])
        else:
            st.chat_message("assistant").markdown(turn["text"])

    prompt2 = st.chat_input("Cola a mensagem que recebeste...")
    if prompt2:
        st.session_state.chat_respostas.append({"role": "user", "text": prompt2})
        st.chat_message("user").markdown(prompt2)

        answer2 = call_openai_chat(SYSTEM_PROMPT_RESPOSTAS, st.session_state.chat_respostas, prompt2, temperature=0.6)
        
        st.session_state.chat_respostas.append({"role": "assistant", "text": answer2})
        st.chat_message("assistant").markdown(answer2)

        
        st.markdown("**Opções (copiar/colar para usar):**")
        st.text_area("Sugestões (seleciona e copia)", value=answer2, height=180)


with tabs[2]:
    st.markdown("### 🎨 " + tab3_label)
    st.write("Responde às perguntas e envie uma selfie. Depois criamos uma descrição artística da tua Alma Gémea — podes pedir para gerar a imagem com IA (integração opcional).")

    with st.form("alma_form", clear_on_submit=False):
        nome = st.text_input("Nome (opcional)")
        idade_desejada = st.number_input("Idade desejada da Alma Gémea", min_value=16, max_value=120, value=28)
        altura = st.text_input("Altura (ex.: 1.75 m)")
        cor_favorita = st.text_input("Cor favorita")
        hobbies = st.text_input("Hobbies (separa por vírgulas, ex.: música, surf, leitura)")
        profissao = st.text_input("Profissão")
        selfie_file = st.file_uploader("Envia uma selfie (jpg/png) — será usada para inspirar a paleta/estilo", type=["jpg","jpeg","png"])
        submitted_alma = st.form_submit_button("Gerar descrição da Alma Gémea (pré-visualização gratuita)")

    if submitted_alma:
        if not selfie_file:
            st.warning("Por favor, envie uma selfie para construir a pré-visualização.")
        else:
          
            img = Image.open(selfie_file).convert("RGB")
            thumb = ImageOps.fit(img, (240,240))
            st.image(thumb, caption="Selfie enviada (apenas para referência visual)")

            
            prompt_text = (
                f"Cria uma descrição fotorrealista e empática de uma 'alma gémea' para alguém chamado '{nome or 'Pessoa'}'. "
                f"Idade aproximada: {idade_desejada}. Altura: {altura}. Cor favorita: {cor_favorita}. "
                f"Hobbies: {hobbies}. Profissão: {profissao}. "
                "A descrição deve ser calorosa, com detalhes sensoriais (cabelo, sorriso, olhar, estilo), "
                "e incluir 1 sugestão de look e 1 ideia de encontro ideal. Mantém 3-5 frases."
            )

            if USE_OPENAI:
                try:
                    resp = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=[{"role":"system","content":"You are a creative portrait writer."},
                                  {"role":"user","content":prompt_text}],
                        max_tokens=200,
                        temperature=0.8
                    )
                    description = resp.choices[0].message.content.strip()
                except Exception as e:
                    description = "Erro ao gerar a descrição com a API de IA. ( " + str(e) + " )"
            else:
                
                description = ("Uma pessoa com sorriso sereno e olhar curioso, estilo casual-chique, "
                               "gosta de longas conversas e passeios ao ar livre. "
                               "Sugestão de look: camisa leve e jeans. Ideal: um café ao pôr do sol.")

            st.markdown("**Descrição gerada (pré-visualização):**")
            st.write(description)

            
            img_prompt = (
                f"Photorealistic portrait of a {idade_desejada}-year-old, {altura} tall, {profissao}, "
                f"hobbies: {hobbies}. Color palette inspired by {cor_favorita}. Warm, soft lighting, subtle smile."
            )
            st.markdown("**Prompt (pronto para geração de imagem IA):**")
            st.code(img_prompt, language="text")

            st.info("Para gerar a imagem final (HD) por IA será necessário pagamento/integrar serviço de geração de imagens. Podemos integrar quando quiseres.")


with tabs[3]:
    st.markdown("### 👶 " + tab4_label)
    st.write("Envie 3 fotos suas e 3 do parceiro(a). A app pode gerar possibilidades artísticas de filhos (requer integração IA / pagamento).")
    fotos_user = st.file_uploader("Envie 3 fotos suas", accept_multiple_files=True, type=["jpg","png","jpeg"], key="f_user")
    fotos_partner = st.file_uploader("Envie 3 fotos do parceiro(a)", accept_multiple_files=True, type=["jpg","png","jpeg"], key="f_partner")

    if st.button("Pré-visualizar combinação (demo)"):
        if len(fotos_user) < 3 or len(fotos_partner) < 3:
            st.warning("Envie pelo menos 3 fotos suas e 3 do parceiro(a) para melhor resultado.")
        else:
            
            cols = st.columns(3)
            for i in range(3):
                uimg = Image.open(fotos_user[i]).convert("RGB")
                pimg = Image.open(fotos_partner[i]).convert("RGB")
                cols[i].image(uimg.resize((200,200)), caption=f"Tu #{i+1}")
                cols[i].image(pimg.resize((200,200)), caption=f"Parceiro(a) #{i+1}")
            st.info("Pré-visualização demo criada. A geração real de filhos em alta qualidade requer IA e pagamento.")


st.markdown("---")
st.markdown("**Nota:** Para chat com qualidade ChatGPT, define `OPENAI_API_KEY` nas variáveis de ambiente (ou nos Secrets do Streamlit). "
            "Se preferires, eu posso integrar também a geração de imagens (Stable Diffusion / Replicate / OpenAI Images) — diz-me qual serviço preferes e eu adapto o código.")
