import os
import asyncio
import edge_tts

async def generate_voice_async(text, video_id):
    output_path = f'/app/output/{video_id}_voice.mp3'
    communicate = edge_tts.Communicate(text, 'id-ID-ArdiNeural')
    await communicate.save(output_path)
    return output_path

def generate_voice(text, video_id):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(generate_voice_async(text, video_id))
