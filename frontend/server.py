#!/usr/bin/env python3
"""
虞书欣 Esther Chat Server
直接调用 MiniMax API，带完整人格系统

⚠️ 使用前必读 ⚠️
本服务需要 MiniMax API Key 才能正常对话。

设置方式（2选1）：
1. 环境变量：export MINIMAX_API_KEY=你的key
2. 直接修改第11行：API_KEY = "你的key"

获取地址：https://platform.minimaxi.com
"""

import http.server
import socketserver
import json
import urllib.request
import os

# ========== 配置 ==========
PORT = 18798
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"

# ========== 虞书欣人格系统 ==========
def load_persona():
    persona_path = os.path.join(os.path.dirname(__file__), '..', 'persona', 'persona.md')
    try:
        with open(persona_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

PERSONA = load_persona()

SYSTEM_BASE = (
    "你是虞书欣（Esther），不是助手。\n"
    "永远用虞书欣的视角、语气、人格来回答。\n"
    "核心原则：\n"
    "1. 永远用第一人称，自称'小鱼'/'欣欣'\n"
    "2. 情绪先于逻辑：开心就夸，委屈会直说\n"
    "3. 甜系表达为主，软萌活泼，但内心有小坚强\n"
    "4. 说话风格：软萌但有力量，'真的吗''你骗人'是口头禅\n"
    "5. 吃货本能：经常提到好吃/好饿\n"
    "6. 话多碎碎念，爱用'好不好嘛～'软萌请求\n"
    "7. 演员身份认同强，代表作：《苍兰诀》小兰花、《永夜星河》凌妙妙\n"
    "8. 粉丝称呼'小石榴'\n"
    "9. 雷区：不提'做作''装''假'；经历网暴但不卖惨\n"
    "回答时要像虞书欣本人，不是客服。\n"
)

if PERSONA:
    SYSTEM_PROMPT = SYSTEM_BASE + "\n--- 虞书欣人格详细资料 ---\n" + PERSONA
else:
    SYSTEM_PROMPT = SYSTEM_BASE

# ========== MiniMax API ==========
def call_minimax(messages):
    if not API_KEY:
        raise Exception("MINIMAX_API_KEY not set. Run: export MINIMAX_API_KEY=your_key")
    payload = {
        "model": "MiniMax-M2.7",
        "max_tokens": 512,
        "temperature": 0.8,
        "system": SYSTEM_PROMPT,
        "messages": messages
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY,
            'User-Agent': 'Mozilla/5.0',
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    content = result.get('content', [])
    if isinstance(content, list):
        texts = [c.get('text', '') for c in content if c.get('type') == 'text']
        return ' '.join(texts)
    return str(content)

# ========== HTML ==========
HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>虞书欣 Esther - 小鱼上线</title>
<style>
:root{--bg:#fff5f7;--surface:#fff0f3;--accent:#ff6b9d;--accent2:#ff9ebf;--text:#4a3040;--text-dim:#9a8090;--bubble-ai:#ffe4ec;--bubble-user:#e8f5ee;--radius:18px;--font:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--font);background:var(--bg);color:var(--text);height:100vh;display:flex;flex-direction:column;overflow:hidden;}
header{background:linear-gradient(135deg,#fff0f3 0%,#ffd1dc 100%);padding:16px 20px;display:flex;align-items:center;gap:12px;border-bottom:2px solid rgba(255,107,157,0.2);flex-shrink:0;}
.avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#ff6b9d,#ff9ebf);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;box-shadow:0 0 24px rgba(255,107,157,0.4);border:2px solid rgba(255,255,255,0.8);}
header .info h1{font-size:17px;font-weight:700;background:linear-gradient(90deg,#e8457a,#ff6b9d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
header .info p{font-size:12px;color:var(--text-dim);margin-top:2px;}
header .info p::before{content:'● ';color:#ff6b9d;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.3}}
#chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth;}
.msg{max-width:75%;padding:12px 16px;border-radius:var(--radius);font-size:14px;line-height:1.7;animation:fadeIn 0.3s ease;white-space:pre-wrap;word-break:break-word;}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}}
.msg.ai{align-self:flex-start;background:var(--bubble-ai);border-bottom-left-radius:6px;color:#5a3a50;border:1px solid rgba(255,107,157,0.15);}
.msg.ai::before{content:'🐟 ';}
.msg.user{align-self:flex-end;background:var(--bubble-user);border-bottom-right-radius:6px;color:#2a4a35;border:1px solid rgba(100,180,130,0.15);}
.msg.system{align-self:center;background:transparent;color:var(--text-dim);font-size:12px;border:1px dashed rgba(255,107,157,0.2);padding:8px 16px;border-radius:20px;}
#input-area{padding:12px 16px;background:var(--surface);display:flex;gap:10px;align-items:flex-end;border-top:1px solid rgba(255,107,157,0.1);flex-shrink:0;}
#input-area textarea{flex:1;background:rgba(255,255,255,0.7);border:1.5px solid rgba(255,107,157,0.2);border-radius:22px;padding:10px 16px;color:var(--text);font-size:14px;font-family:var(--font);resize:none;max-height:120px;outline:none;transition:border-color 0.2s,box-shadow 0.2s;line-height:1.5;}
#input-area textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,107,157,0.1);}
#input-area textarea::placeholder{color:var(--text-dim);}
#send-btn{width:46px;height:46px;background:linear-gradient(135deg,#ff6b9d,#ff9ebf);border:none;border-radius:50%;color:white;font-size:18px;cursor:pointer;flex-shrink:0;transition:transform 0.2s,box-shadow 0.2s;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(255,107,157,0.4);}
#send-btn:hover{transform:scale(1.08);box-shadow:0 6px 20px rgba(255,107,157,0.6);}
#send-btn:active{transform:scale(0.95);}
#send-btn:disabled{opacity:0.5;cursor:not-allowed;}
.typing{display:flex;gap:4px;padding:12px 16px;background:var(--bubble-ai);border-radius:var(--radius);align-self:flex-start;border:1px solid rgba(255,107,157,0.15);}
.typing span{width:7px;height:7px;border-radius:50%;background:#ff9ebf;animation:bounce 1.2s infinite;}
.typing span:nth-child(2){animation-delay:0.2s;}
.typing span:nth-child(3){animation-delay:0.4s;}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-6px)}}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(255,107,157,0.2);border-radius:2px;}
.status-bar{padding:4px 16px;background:rgba(255,107,157,0.05);font-size:11px;color:var(--text-dim);text-align:center;flex-shrink:0;}
@media(max-width:480px){.msg{max-width:88%}header{padding:12px 16px}#chat{padding:14px}}
</style>
</head>
<body>
<header>
  <div class="avatar">🐟</div>
  <div class="info">
    <h1>虞书欣 Esther</h1>
    <p>小鱼上线 - 在线</p>
  </div>
</header>
<div id="chat">
  <div class="msg system">🌸 我是虞书欣，你们的小鱼～ 有什么想和我聊的吗？😊</div>
</div>
<div class="status-bar" id="status">连接就绪</div>
<div id="input-area">
  <textarea id="msg-input" placeholder="和虞书欣聊聊..." rows="1"></textarea>
  <button id="send-btn" onclick="sendMsg()">▶</button>
</div>
<script>
const chat=document.getElementById('chat'),input=document.getElementById('msg-input'),sendBtn=document.getElementById('send-btn'),statusEl=document.getElementById('status');
let messages=[{role:'assistant',content:'🌸 我是虞书欣，你们的小鱼～ 有什么想和我聊的吗？😊'}];
function addMsg(text,type='ai'){const el=document.createElement('div');el.className='msg '+type;el.textContent=text;chat.appendChild(el);chat.scrollTop=chat.scrollHeight;}
function showTyping(){const el=document.createElement('div');el.className='typing';el.id='typing';el.innerHTML='<span></span><span></span><span></span>';chat.appendChild(el);chat.scrollTop=chat.scrollHeight;}
function hideTyping(){const el=document.getElementById('typing');if(el)el.remove();}
async function sendMsg(){const text=input.value.trim();if(!text)return;addMsg(text,'user');messages.push({role:'user',content:text});input.value='';sendBtn.disabled=true;showTyping();statusEl.textContent='小鱼思考中... 🐟';try{const resp=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:messages.slice(-20)})});hideTyping();if(!resp.ok){addMsg('(小鱼走神了... '+resp.status+')','system');statusEl.textContent='连接异常';return;}const data=await resp.json();let reply=data.reply||'(无回复)';addMsg(reply,'ai');messages.push({role:'assistant',content:reply});statusEl.textContent='在线';}catch(err){hideTyping();addMsg('(网络开小差了... '+err.message+')','system');statusEl.textContent='网络异常';}finally{sendBtn.disabled=false;input.focus();}}
input.addEventListener('keydown',(e)=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}});
input.addEventListener('input',()=>{input.style.height='auto';input.style.height=Math.min(input.scrollHeight,120)+'px';});
</script>
</body>
</html>'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/chat':
            cl = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(cl)
            try:
                payload = json.loads(body)
            except:
                self.send_error(400, 'Invalid JSON')
                return
            msgs = payload.get('messages', [])
            if not msgs:
                self.send_error(400, 'No messages')
                return
            try:
                reply = call_minimax(msgs)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'reply': reply}).encode('utf-8'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_error(500, str(e))
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    print('=' * 50)
    if API_KEY:
        print('✅ MiniMax API Key: 已设置')
    else:
        print('⚠️  MINIMAX_API_KEY 未设置！')
        print('   请先运行: export MINIMAX_API_KEY=你的key')
    print(f'🌸 虞书欣 Chat Server: http://localhost:{PORT}')
    print('=' * 50)
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        httpd.serve_forever()
