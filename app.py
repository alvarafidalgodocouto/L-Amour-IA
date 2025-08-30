import streamlit as st
from openai import OpenAI
from PIL import Image
import paypalrestsdk
import uuid

# Config
st.set_page_config(page_title="Love Advice AI App 💕", layout="wide")

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# PayPal config
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": st.secrets["PAYPAL_CLIENT_ID"],
    "client_secret": st.secrets["PAYPAL_CLIENT_SECRET"]
})

# Lightweight translator
@st.cache_data
def translate_text(text, target_lang="EN"):
    if target_lang == "EN":
        return text
    prompt = f"Translate the following text to {target_lang} keeping the same meaning and tone:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Chat AI function
def chat_response(prompt, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# PayPal payment function
def create_payment(amount, description, return_url="https://www.google.com", cancel_url="https://www.google.com"):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": description,
                    "sku": str(uuid.uuid4()),
                    "price": str(amount),
                    "currency": "EUR",
                    "quantity": 1
                }]
            },
            "amount": {"total": str(amount), "currency": "EUR"},
            "description": description
        }]
    })
    if payment.create():
        return payment.links[1].href
    else:
        return None

# Language selector
language = st.selectbox("Choose language 🌐", options=["EN", "PT", "ES", "FR", "DE"])

# --- Header ---
st.title(translate_text("💘 Love Advice & Personalized AI Services", language))
st.markdown(translate_text(
    "Welcome! This app offers 4 unique services to help with love, communication, and visualization of your future family.", language))

# --- Mobile-friendly "tabs" ---
service = st.radio(
    translate_text("Select a service", language),
    options=[
        translate_text("💌 Love Advice Chat", language),
        translate_text("💬 Message Reply Suggestions", language),
        translate_text("✨ Discover Your Soulmate", language),
        translate_text("👶 Visualize Your Children", language)
    ]
)

# --- Service 1: Love Advice Chat ---
if service == translate_text("💌 Love Advice Chat", language):
    st.subheader(translate_text("Get personalized love advice from our AI therapist.", language))
    if "chat1" not in st.session_state:
        st.session_state.chat1 = []

    for msg in st.session_state.chat1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input(translate_text("Share your feelings...", language)):
        st.session_state.chat1.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = chat_response(user_input, translate_text(
            "You are an empathetic therapist giving human love advice.", language))
        st.session_state.chat1.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- Service 2: Message Reply Suggestions ---
elif service == translate_text("💬 Message Reply Suggestions", language):
    st.subheader(translate_text("Paste a message and get expert reply suggestions.", language))
    if "chat2" not in st.session_state:
        st.session_state.chat2 = []

    for msg in st.session_state.chat2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input2 := st.chat_input(translate_text("Paste the message here...", language)):
        st.session_state.chat2.append({"role": "user", "content": user_input2})
        with st.chat_message("user"):
            st.markdown(user_input2)

        response2 = chat_response(user_input2, translate_text(
            "You are a love communication expert. Help create an empathetic, romantic, natural reply.", language))
        st.session_state.chat2.append({"role": "assistant", "content": response2})
        with st.chat_message("assistant"):
            st.markdown(response2)

# --- Service 3: Discover Soulmate ---
elif service == translate_text("✨ Discover Your Soulmate", language):
    st.subheader(translate_text("Discover your soulmate and see a personalized AI drawing.", language))
    st.markdown(translate_text("Fill in your details and upload a selfie to generate your soulmate.", language))

    name = st.text_input(translate_text("Your name:", language))
    age = st.number_input(translate_text("Your age:", language), min_value=16, max_value=100, step=1)
    height = st.text_input(translate_text("Your height:", language))
    fav_color = st.text_input(translate_text("Your favorite color:", language))
    hobbies = st.text_area(translate_text("Your hobbies:", language))
    profession = st.text_input(translate_text("Your profession:", language))
    selfie = st.file_uploader(translate_text("Upload a selfie 📷", language), type=["jpg", "png", "jpeg"])

    if st.button(translate_text("Pay 1€ to generate soulmate 💕", language)):
        link_payment = create_payment(1, "Soulmate Drawing")
        if link_payment:
            st.markdown(f"[👉 Click here to pay with PayPal and receive your soulmate]({link_payment})")
        else:
            st.error(translate_text("Payment error. Check PayPal credentials.", language))

    if name and age and height and fav_color and hobbies and profession and selfie:
        st.info(translate_text("⚠️ After payment, we will generate your soulmate!", language))
        img = Image.open(selfie)
        st.image(img, caption="(Your selfie uploaded)")

# --- Service 4: Visualize Children ---
elif service == translate_text("👶 Visualize Your Children", language):
    st.subheader(translate_text("Visualize how your future children might look.", language))
    st.markdown(translate_text("Upload 3 photos of yourself and 3 photos of the other person.", language))

    your_photos = st.file_uploader(translate_text("Your 3 photos", language), type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    other_photos = st.file_uploader(translate_text("The other person's 3 photos", language), type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if st.button(translate_text("Pay 2€ and see the results 👶💕", language)):
        link_payment2 = create_payment(2, "Children Visualization")
        if link_payment2:
            st.markdown(f"[👉 Click here to pay with PayPal and see your children]({link_payment2})")
        else:
            st.error(translate_text("Payment error. Check PayPal credentials.", language))

    if your_photos and other_photos:
        if len(your_photos) == 3 and len(other_photos) == 3:
            st.info(translate_text("⚠️ After payment, we will generate realistic images of the children based on uploaded photos.", language))
            for f in your_photos + other_photos:
                img = Image.open(f)
                st.image(img, width=150)
        else:
            st.warning(translate_text("You must upload exactly 3 photos of yourself and 3 of the other person.", language))
