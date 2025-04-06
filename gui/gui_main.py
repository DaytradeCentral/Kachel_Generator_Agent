import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from generator.image_generator import KachelImageGenerator
from gpt.ci_gpt import GPTKachelAgent
from config import FORMATS
from PIL import Image
import io

st.set_page_config(page_title="Kachel Generator", layout="centered")
st.title("🧱 AfD Kachel Generator")
st.markdown("Erzeuge Social Media Kacheln im AfD-Design – mit optionalen GPT-Vorschlägen.")

# Formatwahl
format_choice = st.selectbox("Format wählen", options=list(FORMATS.keys()))
size = FORMATS[format_choice]

# Strahlen?
rays = st.checkbox("Strahlen hinzufügen", value=True)

# GPT-Vorschlag
use_gpt = st.checkbox("GPT-Vorschlag holen", value=False)

headline = st.text_input("🔷 Headline", "")
subline = st.text_input("🔹 Subline", "")
stoerer = st.text_input("🔴 Störertext", "")

if use_gpt:
    topic = st.text_input("💡 Thema für GPT (z. B. Energie, Migration, Wirtschaft):", "")
    if st.button("🧠 Vorschlag holen"):
        gpt = GPTKachelAgent()
        prompt = f"Erstelle eine AfD-Kachel im Format {format_choice.upper()} zum Thema {topic}. Gib JSON mit headline, subline, stoerer zurück."
        result = gpt.prompt(prompt)
        headline = result.get("headline", "")
        subline = result.get("subline", "")
        stoerer = result.get("stoerer", "")
        st.success("Vorschlag übernommen.")

# Bild erzeugen
if st.button("🎨 Kachel erzeugen"):
    generator = KachelImageGenerator(*size)
    base = generator.generate_gradient()
    if rays:
        image = generator.add_rays(base)
    else:
        image = base
    final = generator.draw_text(image, headline, subline, stoerer)
    st.image(final, caption="Vorschau", use_container_width=True)

    # Download-Button
    buf = io.BytesIO()
    final.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="💾 Download als PNG",
        data=byte_im,
        file_name=f"kachel_{format_choice}.png",
        mime="image/png"
    )
