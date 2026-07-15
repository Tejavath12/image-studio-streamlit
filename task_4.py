import streamlit as st
import requests
import random
from urllib.parse import quote
from datetime import datetime

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

st.title("🎨 AI IMAGE STUDIO")
st.caption("Generate stunning AI images with customizable styles.")

if "history" not in st.session_state:
    st.session_state.history = []


st.sidebar.header("⚙️ Settings")

style_prompts = {
    "Photorealistic": "ultra realistic, DSLR photography, highly detailed",
    "Cinematic": "cinematic lighting, dramatic atmosphere",
    "Anime": "anime style, vibrant colors",
    "Disney Pixar": "Disney Pixar 3D animation",
    "Studio Ghibli": "Studio Ghibli artwork",
    "Cyberpunk": "cyberpunk city, neon lights",
    "Fantasy Art": "epic fantasy artwork",
    "Sci-Fi": "science fiction futuristic technology",
    "Oil Painting": "classic oil painting",
    "Watercolor": "soft watercolor painting",
    "Pencil Sketch": "realistic pencil sketch",
    "Pixel Art": "8-bit pixel art",
    "3D Render": "high quality 3D render",
    "Comic Book": "comic illustration",
    "Minimalist": "minimalist clean design"
}

art_style = st.sidebar.selectbox(
    "Art Style",
    list(style_prompts.keys())
)

width = st.sidebar.slider("Width", 256, 1024, 768)
height = st.sidebar.slider("Height", 256, 1024, 768)

magic = st.sidebar.checkbox("✨ Enable Magic Enhance")

st.sidebar.divider()

uploaded_image = st.sidebar.file_uploader(
    "📤 Upload Reference Image",
    type=["png", "jpg", "jpeg"]
)



if uploaded_image:
    st.image(uploaded_image, caption="Reference Image", width=250)

user_prompt = st.text_input(
    "Describe your image"
)

surprise_prompts = [
    "Astronaut riding a horse on Mars",
    "Cyberpunk street food market",
    "Floating castle above the clouds",
    "Dragon reading books in a library",
    "Robot painting a sunset"
]


def generate(prompt):

    full_prompt = f"{prompt}, {style_prompts[art_style]}"

    if magic:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded = quote(full_prompt)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={width}&height={height}"
    )

    with st.spinner("Generating Image..."):
        response = requests.get(url)

    if response.status_code == 200:

        st.success("✅ Image Generated")

        st.image(
            response.content,
            caption=prompt,
            use_container_width=True
        )

        st.download_button(
            "📥 Download Image",
            response.content,
            file_name=f"{art_style}_image.png",
            mime="image/png"
        )

        st.session_state.history.append({
            "prompt": prompt,
            "time": datetime.now().strftime("%H:%M:%S")
        })

    else:
        st.error("Image generation failed.")


col1, col2 = st.columns(2)

with col1:
    if st.button("🎨 Generate Image", use_container_width=True):

        if user_prompt.strip():

            generate(user_prompt)

        else:

            st.warning("Enter a prompt first.")

with col2:
    if st.button("🎲 Surprise Me!", use_container_width=True):

        random_prompt = random.choice(surprise_prompts)

        st.info(random_prompt)

        generate(random_prompt)



if st.session_state.history:

    st.divider()

    st.subheader("🕘 Recent Prompts")

    for item in reversed(st.session_state.history):

        st.write(f"**{item['time']}** — {item['prompt']}")