import streamlit as st
from PIL import Image
import io
import tempfile
import os
from realesrgan import RealESRGAN
import torch

# Initialize Streamlit
st.set_page_config(page_title="AI Upscale & GIF Maker", layout="centered")
st.title("🧠 AI Image Upscaler & GIF Creator")

# Upload images
uploaded_files = st.file_uploader(
    "Upload images (JPG or PNG):",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Optional upscale dimensions
st.subheader("Optional: Target Dimensions for Upscaling")
target_width = st.number_input("Target Width (px)", min_value=1, value=0)
target_height = st.number_input("Target Height (px)", min_value=1, value=0)
st.caption("Note: Only one will be used to maintain aspect ratio. If both are filled, width will be used.")

# Frame duration
duration = st.slider("Frame duration (ms)", min_value=100, max_value=2000, value=500, step=100)

# Real-ESRGAN model loading (once)
@st.cache_resource
def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('RealESRGAN_x4.pth', download=True)
    return model

# Resize with aspect ratio
def resize_keep_aspect(image, target_w=0, target_h=0):
    original_w, original_h = image.size
    if target_w > 0 and target_h == 0:
        ratio = target_w / original_w
        return image.resize((target_w, int(original_h * ratio)), Image.LANCZOS)
    elif target_h > 0 and target_w == 0:
        ratio = target_h / original_h
        return image.resize((int(original_w * ratio), target_h), Image.LANCZOS)
    elif target_h > 0 and target_w > 0:
        st.warning("Both width and height specified — using only width.")
        ratio = target_w / original_w
        return image.resize((target_w, int(original_h * ratio)), Image.LANCZOS)
    else:
        return image

if uploaded_files:
    model = load_model()

    upscaled_images = []
    st.subheader("Upscaled Image Previews")

    for file in uploaded_files:
        image = Image.open(file).convert("RGB")
        image = resize_keep_aspect(image, target_width, target_height)

        # Real-ESRGAN upscale
        with st.spinner(f"Upscaling {file.name}..."):
            upscaled = model.predict(image)
            upscaled_images.append(upscaled)

    st.image(upscaled_images, width=150)

    if st.button("🎬 Create GIF"):
        if len(upscaled_images) > 1:
            gif_bytes = io.BytesIO()
            upscaled_images[0].save(
                gif_bytes,
                format="GIF",
                save_all=True,
                append_images=upscaled_images[1:],
                duration=duration,
                loop=0
            )
            gif_bytes.seek(0)

            st.success("GIF created successfully!")
            st.image(gif_bytes, caption="Animated GIF", use_column_width=True)

            st.download_button(
                label="⬇️ Download GIF",
                data=gif_bytes,
                file_name="ai_upscaled_output.gif",
                mime="image/gif"
            )
        else:
            st.warning("Upload at least two images to create a GIF.")
else:
    st.info("Upload images to get started.")
