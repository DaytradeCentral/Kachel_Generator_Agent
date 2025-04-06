import streamlit as st
from generator.image_generator import KachelImageGenerator
from gpt.ci_gpt import GPTKachelAgent
from config import FORMATS
from PIL import Image

st.set_page_config(page_title="Kachel Generator", layout="centered")

st.title("🧱 AfD Kachel Generator")
st.markdown("Erzeuge Social Media Kacheln im AfD-Design – mit optionalen GPT-Vorschlägen.")

# Formatwahl
format_choice = st.selectbox("Format wählen", options=list(FORMATS.keys()))
size = FORMATS[format_choice]

# Strahlen?
rays = st.checkbox("Strahlen hinzufügen", value=True)

# GPT-Integration
use_gpt = st.checkbox("GPT-Vorschlag holen")
headline = ""
if use_gpt:
    gpt = GPTKachelAgent()
    topic = st.text_input("Thema für GPT (z. B. Energie, Migration, Wirtschaft):", "")
    if st.button("🧠 Vorschlag holen"):
        prompt = f"Erstelle eine knackige Headline für eine Kachel im Format {format_choice.upper()} zum Thema {topic}."
        headline = gpt.prompt(prompt)
        st.success("GPT-Antwort: " + headline)

# Bild erzeugen
if st.button("🎨 Kachel erzeugen"):
    generator = KachelImageGenerator(*size)
    base = generator.generate_gradient()
    if rays:
        image = generator.add_rays(base)
    else:
        image = base
    filename = f"assets/exports/kachel_{format_choice}.png"
    generator.save_image(image, filename)
    st.image(image, caption="Erzeugte Kachel", use_column_width=True)
    st.success(f"Kachel gespeichert unter: {filename}")
