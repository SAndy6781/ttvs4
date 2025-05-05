import os
import imageio_ffmpeg as ffmpeg
# Tell MoviePy to use the ffmpeg binary from imageio-ffmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg.get_ffmpeg_exe()

import streamlit as st
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import tempfile
import uuid

def create_slide_image(text, width=1280, height=720):
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    text_w, text_h = draw.textsize(text, font=font)
    draw.text(
        ((width - text_w) / 2, (height - text_h) / 2),
        text,
        font=font,
        fill=(255, 255, 255)
    )
    temp_img_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.png")
    img.save(temp_img_path)
    return temp_img_path

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp3")
    tts.save(audio_path)
    return audio_path

def generate_video_from_text(text):
    img_path = create_slide_image(text)
    audio_path = text_to_speech(text)
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(img_path).set_duration(audio_clip.duration)

    video = image_clip.set_audio(audio_clip)
    output_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp4")
    video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    return output_path

st.title("📝➡️🎬 Text to Video Converter")
user_text = st.text_area("Enter your text here", height=200)

if st.button("Generate Video"):
    with st.spinner("Creating your video..."):
        video_path = generate_video_from_text(user_text)
        st.video(video_path)
        with open(video_path, "rb") as f:
            st.download_button("Download Video", f, file_name="output_video.mp4")
