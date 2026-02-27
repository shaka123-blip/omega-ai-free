import os
import uuid
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template_string

app = Flask(__name__)

for d in ['data', 'output', 'cache']:
    os.makedirs(f'/app/{d}', exist_ok=True)

DB_FILE = '/app/data/videos.json'

def load_videos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_video(video):
    videos = load_videos()
    videos.append(video)
    with open(DB_FILE, 'w') as f:
        json.dump(videos, f)

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OMEGA AI Free - shaka123-blip</title>
    <style>
        body{font-family:system-ui,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;color:#fff;margin:0;padding:20px}
        .container{max-width:800px;margin:0 auto}
        .header{text-align:center;padding:40px 0}
        .header h1{font-size:3em;margin:0}
        .user-badge{background:rgba(255,255,255,0.2);display:inline-block;padding:5px 15px;border-radius:20px;margin-top:15px;font-size:0.9em}
        .card{background:rgba(255,255,255,0.1);border-radius:20px;padding:30px;margin:20px 0}
        .form-group{margin-bottom:20px}
        label{display:block;margin-bottom:8px;font-weight:600}
        select{width:100%;padding:12px;border-radius:10px;border:none;background:rgba(255,255,255,0.2);color:#fff;font-size:16px}
        select option{background:#333}
        button{background:linear-gradient(135deg,#f093fb,#f5576c);border:none;padding:15px 40px;border-radius:30px;color:#fff;font-size:18px;font-weight:600;cursor:pointer;width:100%}
        button:disabled{opacity:0.6}
        .progress{display:none;margin-top:20px;padding:20px;background:rgba(0,0,0,0.2);border-radius:15px}
        .progress.active{display:block}
        .step{padding:15px;margin:10px 0;background:rgba(255,255,255,0.1);border-radius:10px;opacity:0.5}
        .step.active{opacity:1;background:rgba(255,255,255,0.2)}
        .step.done{opacity:1;background:#10b981}
        .result{display:none;margin-top:20px;padding:25px;background:rgba(255,255,255,0.1);border-radius:15px;text-align:center}
        .result.active{display:block}
        .success-icon{width:60px;height:60px;background:#10b981;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:30px}
        video{width:100%;max-width:400px;border-radius:15px;margin:20px 0}
        .download-btn{display:inline-block;background:#10b981;color:#fff;padding:12px 30px;border-radius:25px;text-decoration:none;margin-top:10px}
        .video-list{margin-top:20px}
        .video-item{background:rgba(255,255,255,0.1);padding:15px;margin:10px 0;border-radius:10px;display:flex;justify-content:space-between;align-items:center;gap:15px}
        .empty{text-align:center;padding:40px;opacity:0.7}
        .footer{text-align:center;padding:40px 0;opacity:0.8;font-size:0.9em}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 OMEGA AI</h1>
            <p>100% Free Content Generator</p>
            <div class="user-badge">👤 shaka123-blip</div>
        </div>
        
        <div class="card">
            <h2>✨ Generate Video</h2>
            <div class="form-group">
                <label>Channel</label>
                <select id="channel">
                    <option value="MotivasiHarian">Motivasi Harian</option>
                    <option value="CeritaHidup">Cerita Hidup</option>
                </select>
            </div>
            <div class="form-group">
                <label>Niche</label>
                <select id="niche">
                    <option value="motivasi">Motivasi Islami</option>
                    <option value="inspirasi">Kisah Inspiratif</option>
                </select>
            </div>
            <button id="btn" onclick="generate()">Generate Video</button>
            
            <div class="progress" id="progress">
                <div class="step active" id="s1">1. AI Script Generation</div>
                <div class="step" id="s2">2. Voice Synthesis</div>
                <div class="step" id="s3">3. Video Rendering</div>
            </div>
            
            <div class="result" id="result">
                <div class="success-icon">✓</div>
                <h3 style="color:#10b981">Video Ready!</h3>
                <video id="vid" controls></video>
                <div id="title" style="font-weight:600;margin:10px 0"></div>
                <a href="#" class="download-btn" id="dl" download>⬇️ Download MP4</a>
            </div>
        </div>
        
        <div class="card">
            <h2>🎥 Recent Videos</h2>
            <div id="list" class="video-list"><div class="empty">No videos yet</div></div>
        </div>
        
        <div class="footer">
            <p>OMEGA AI Free | Deployed by shaka123-blip</p>
            <p>Made with ❤️ on Hugging Face Spaces</p>
        </div>
    </div>
    
    <script>
        async function generate(){
            document.getElementById('btn').disabled=true;
            document.getElementById('progress').classList.add('active');
            document.getElementById('result').classList.remove('active');
            
            const params={
                channel:document.getElementById('channel').value,
                niche:document.getElementById('niche').value
            };
            
            setStep(1,'active');
            await sleep(2000);
            setStep(1,'done');
            
            setStep(2,'active');
            await sleep(2000);
            setStep(2,'done');
            
            setStep(3,'active');
            
            const res=await fetch('/api/generate',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify(params)
            });
            
            const data=await res.json();
            setStep(3,'done');
            
            if(data.success){
                showResult(data.video);
                loadVideos();
            }
            
            document.getElementById('btn').disabled=false;
            setTimeout(()=>document.getElementById('progress').classList.remove('active'),2000);
            resetSteps();
        }
        
        function setStep(n,status){
            document.getElementById('s'+n).className='step '+status;
        }
        
        function resetSteps(){
            for(let i=1;i<=3;i++)document.getElementById('s'+i).className='step'+(i===1?' active':'');
        }
        
        function showResult(v){
            document.getElementById('result').classList.add('active');
            document.getElementById('vid').src=v.url;
            document.getElementById('title').textContent=v.title;
            document.getElementById('dl').href=v.url;
        }
        
        async function loadVideos(){
            const res=await fetch('/api/videos');
            const videos=await res.json();
            const list=document.getElementById('list');
            
            if(videos.length===0){
                list.innerHTML='<div class="empty">No videos yet</div>';
                return;
            }
            
            list.innerHTML=videos.reverse().map(v=>
                <div class="video-item">
                    <div>
                        <div style="font-weight:600"></div>
                        <div style="font-size:0.9em;opacity:0.8"> • </div>
                    </div>
                    <a href="" class="download-btn" style="padding:8px 20px;font-size:0.9em" download>Download</a>
                </div>
            ).join('');
        }
        
        function sleep(ms){return new Promise(r=>setTimeout(r,ms))}
        
        loadVideos();
        setInterval(loadVideos,30000);
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        video_id = str(uuid.uuid4())[:8]
        
        from src.ai_engine import generate_script
        from src.tts_engine import generate_voice
        from src.video_engine import create_video
        
        script = generate_script(data.get('niche', 'motivasi'))
        voice_path = generate_voice(script['text'], video_id)
        video_path = create_video(script, voice_path, video_id)
        
        video = {
            'id': video_id,
            'title': script['title'],
            'channel': data.get('channel', 'MotivasiHarian'),
            'url': f'/api/download/{os.path.basename(video_path)}',
            'created_at': datetime.now().isoformat()
        }
        
        save_video(video)
        return jsonify({'success': True, 'video': video})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/videos')
def list_videos():
    return jsonify(load_videos())

@app.route('/api/download/<filename>')
def download(filename):
    path = os.path.join('/app/output', filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
