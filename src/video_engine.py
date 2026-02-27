import os
from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip, ColorClip

def create_video(script, voice_path, video_id):
    output_path = f'/app/output/{video_id}.mp4'
    
    bg = ColorClip(size=(1080, 1920), color=(30, 30, 60), duration=30)
    
    txt = TextClip(
        script['text'],
        fontsize=60,
        color='white',
        method='caption',
        size=(1000, None),
        align='center'
    ).set_duration(30).set_position('center')
    
    video = CompositeVideoClip([bg, txt])
    
    if os.path.exists(voice_path):
        audio = AudioFileClip(voice_path).subclip(0, 30)
        video = video.set_audio(audio)
    
    video.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        threads=2,
        preset='ultrafast'
    )
    
    return output_path
