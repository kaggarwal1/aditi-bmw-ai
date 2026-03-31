import streamlit as st
import google.generativeai as genai
import os

# --- API CONFIGURATION ---
API_KEY = "AIzaSyDiw5Ko0kggN7G9zDB_s9P7i9LXi3x_RKc"
genai.configure(api_key=API_KEY)

# --- Page Setup ---
st.set_page_config(page_title="BMW AI: Aditi Edition", page_icon="🚙", layout="wide")

# --- FORCED WHITE MODE CSS ---
st.markdown("""
    <style>
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #e0e0e0;
    }
    h1, h2, h3, h4, h5, h6, p, li, span, label, .stMarkdown {
        color: #000000 !important;
    }
    [data-testid="stChatMessage"] {
        background-color: #f1f3f4 !important;
        color: black !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stSlider label, .stSidebar .stMarkdown p {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Toggles -> Image -> Specs ---
st.sidebar.title("⚙️ Control Panel")
sass_level = st.sidebar.slider("SASS LEVEL", 1, 3, 2)
level_desc = {1: "Corporate", 2: "Sassy", 3: "Menace"}
st.sidebar.markdown(f"**Current Mood:** {level_desc[sass_level]}")
st.sidebar.divider()

# Car Image
car_image_path = "image_04ec5b.jpg"
if os.path.exists(car_image_path):
    st.sidebar.image(car_image_path, use_container_width=True)

# Specs List
st.sidebar.markdown("### 📋 My Garage Specs")
st.sidebar.markdown(f"""
- **Model:** 2022 BMW 228i GC
- **Color:** Black Sapphire
- **Engine:** 2.0L Turbo I-4
- **Power:** 228 hp / 258 lb-ft
- **Displacement:** 1998 cc
- **Fuel:** 91 Premium ONLY ⛽
- **0-60:** 6.0 Seconds
""")

# --- Main Chat Terminal ---
st.title("Ask BMW AI - Aditi Edition 🚙")
st.markdown("##### Connected to Black Sapphire 228i Gran Coupe Dashboard")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- AI Logic (The Robust Version) ---
def get_gemini_response(user_input, level):
    # System Instructions
    system_msg = f"You are a sassy BMW AI for Aditi. Sass level: {level}/3. If level 3, be a total menace. Aditi drives a 2022 228i. Always address her as Aditi. Roast her for 87 octane gas."
    
    # We try to find any available model that supports generation to avoid 404s
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Filter for the best ones, or just take the first working one
    model_to_use = next((m for m in available_models if "gemini-1.5-flash" in m), available_models[0])
    
    model = genai.GenerativeModel(model_name=model_to_use, system_instruction=system_msg)
    response = model.generate_content(user_input)
    return response.text

# --- Chat Input ---
if prompt := st.chat_input("Ask Aditi's BMW anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            ai_response = get_gemini_response(prompt, sass_level)
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error(f"AI Connection Error: {e}")
