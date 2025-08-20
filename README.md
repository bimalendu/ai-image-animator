\# 🧠 AI Image Upscaler \& GIF Creator



This is a Streamlit web application that allows users to upload multiple images (JPG or PNG), upscale them using AI (Real-ESRGAN), and combine them into an animated GIF. The app ensures aspect ratio is preserved during resizing, and allows custom frame durations.



---



\## ✨ Features



\- 🖼️ Upload unlimited `.jpg` or `.png` images.

\- 🧠 AI-based upscaling using \[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN).

\- 📏 Optional width or height input (preserves aspect ratio).

\- 🎞️ Combine upscaled images into a high-quality animated GIF.

\- 💾 Download the generated GIF directly from the app.



---



\## 🔧 Installation \& Setup



Follow these steps to set up and run the app locally.

```bash

git clone https://github.com/bimalendu/ai-image-animator.git

cd ai-image-animator

uv init

uv add streamlit

uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

uv add realesrgan

uv run -- streamlit run app.py