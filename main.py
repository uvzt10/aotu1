from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import os
import edge_tts
import requests
from moviepy.editor import *
import asyncio

app = FastAPI()

# إعدادات ثابتة
OUTPUT_FILE = "final_short.mp4"
AUDIO_FILE = "voice.mp3"
IMAGE_FILE = "image.jpg"

async def create_content(topic: str):
    # 1. توليد الصوت (Edge-TTS)
    # صوت أمريكي احترافي
    voice = "en-US-ChristopherNeural" 
    text = f"Here is a crazy fact about {topic}. Did you know that this is one of the most mysterious things in the world? Subscribe for more."
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(AUDIO_FILE)

    # 2. توليد الصورة (Pollinations AI - Free)
    prompt = f"cinematic shot of {topic}, dark atmosphere, 8k, realistic, vertical 9:16 aspect ratio"
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&model=flux"
    
    response = requests.get(url)
    with open(IMAGE_FILE, 'wb') as f:
        f.write(response.content)

    # 3. المونتاج (MoviePy)
    # تحميل الصوت لمعرفة مدة الفيديو
    audio_clip = AudioFileClip(AUDIO_FILE)
    duration = audio_clip.duration

    # إعداد الصورة وتحريكها (Zoom بسيط)
    clip = ImageClip(IMAGE_FILE).set_duration(duration)
    
    # تحريك بسيط (Center Crop) لتبدو متحركة
    # ملاحظة: التحريك المعقد يحتاج وقت رندرة أطول
    clip = clip.resize(height=1920) 
    
    # دمج الصوت
    final_clip = clip.set_audio(audio_clip)
    
    # تصدير الفيديو
    final_clip.write_videofile(OUTPUT_FILE, fps=24, codec="libx264", audio_codec="aac")

@app.get("/")
def read_root():
    return {"status": "Service is Running. Go to /generate?topic=Space to create a video."}

@app.get("/generate")
async def generate_video(topic: str = "Space"):
    """
    رابط لتوليد الفيديو.
    مثال للاستخدام: YOUR_URL/generate?topic=Ghosts
    """
    try:
        await create_content(topic)
        return FileResponse(OUTPUT_FILE, media_type="video/mp4", filename=f"short_{topic}.mp4")
    except Exception as e:
        return {"error": str(e)}
