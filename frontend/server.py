#!/usr/bin/env python3
"""
虞书欣 Esther Chat Server - 虞书欣数字人格对话前端
使用OpenClaw sessions_send工具转发消息
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os

PORT = 18798
GW_TOKEN = os.environ.get("GW_TOKEN", "d42bbfa36521549fe11faef3fa4a5110ec89e1bd1f5be74e")
GW_HOST = os.environ.get("GW_HOST", "127.0.0.1")
GW_PORT_API = int(os.environ.get("GW_PORT_API", "18789"))

# HTML page as string — 虞书欣粉色主题
HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>虞书欣 Esther · 小鱼上线</title>
<style>
:root {
  --bg: #fff5f7;
  --surface: #fff0f3;
  --surface2: #ffe4ec;
  --accent: #ff6b9d;
  --accent2: #ff9ebf;
  --text: #4a3040;
  --text-dim: #9a8090;
  --bubble-ai: #ffe4ec;
  --bubble-user: #e8f5ee;
  --radius: 18px;
  --font: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header */
header {
  background: linear-gradient(135deg, #fff0f3 0%, #ffe4ec 50%, #ffd1dc 100%);
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 2px solid rgba(255,107,157,0.2);
  flex-shrink: 0;
  box-shadow: 0 2px 20px rgba(255,107,157,0.1);
}
.avatar {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b9d, #ff9ebf);
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; flex-shrink: 0;
  box-shadow: 0 0 24px rgba(255,107,157,0.4);
  border: 2px solid rgba(255,255,255,0.8);
}
header .info h1 {
  font-size: 17px; font-weight: 700;
  background: linear-gradient(90deg, #e8457a, #ff6b9d);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
header .info p { font-size: 12px; color: var(--text-dim); margin-top: 2px; }
header .info p::before { content: '● '; color: #ff6b9d; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Messages */
#chat {
  flex: 1; overflow-y: auto; padding: 20px;
  display: flex; flex-direction: column; gap: 12px;
  scroll-behavior: smooth;
}
.msg {
  max-width: 75%; padding: 12px 16px;
  border-radius: var(--radius); font-size: 14px;
  line-height: 1.7; animation: fadeIn 0.3s ease;
  white-space: pre-wrap; word-break: break-word;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } }
.msg.ai {
  align-self: flex-start;
  background: var(--bubble-ai);
  border-bottom-left-radius: 6px;
  color: #5a3a50;
  border: 1px solid rgba(255,107,157,0.15);
}
.msg.ai::before { content: '🐟 '; }
.msg.user {
  align-self: flex-end;
  background: var(--bubble-user);
  border-bottom-right-radius: 6px;
  color: #2a4a35;
  border: 1px solid rgba(100,180,130,0.15);
}
.msg.system {
  align-self: center; background: transparent; color: var(--text-dim);
  font-size: 12px; border: 1px dashed rgba(255,107,157,0.2);
  padding: 8px 16px; border-radius: 20px;
}

/* Input */
#input-area {
  padding: 12px 16px; background: var(--surface);
  display: flex; gap: 10px; align-items: flex-end;
  border-top: 1px solid rgba(255,107,157,0.1); flex-shrink: 0;
}
#input-area textarea {
  flex: 1; background: rgba(255,255,255,0.7);
  border: 1.5px solid rgba(255,107,157,0.2);
  border-radius: 22px; padding: 10px 16px;
  color: var(--text); font-size: 14px; font-family: var(--font);
  resize: none; max-height: 120px; outline: none;
  transition: border-color 0.2s, box-shadow 0.2s; line-height: 1.5;
}
#input-area textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255,107,157,0.1);
}
#input-area textarea::placeholder { color: var(--text-dim); }
#send-btn {
  width: 46px; height: 46px;
  background: linear-gradient(135deg, #ff6b9d, #ff9ebf);
  border: none; border-radius: 50%; color: white;
  font-size: 18px; cursor: pointer; flex-shrink: 0;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 16px rgba(255,107,157,0.4);
}
#send-btn:hover { transform: scale(1.08); box-shadow: 0 6px 20px rgba(255,107,157,0.6); }
#send-btn:active { transform: scale(0.95); }
#send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* Typing indicator */
.typing {
  display: flex; gap: 4px; padding: 12px 16px;
  background: var(--bubble-ai); border-radius: var(--radius);
  align-self: flex-start; border: 1px solid rgba(255,107,157,0.15);
}
.typing span { width: 7px; height: 7px; border-radius: 50%; background: #ff9ebf; animation: bounce 1.2s infinite; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,107,157,0.2); border-radius: 2px; }

/* Status bar */
.status-bar { padding: 4px 16px; background: rgba(255,107,157,0.05); font-size: 11px; color: var(--text-dim); text-align: center; flex-shrink: 0; }

/* Mobile */
@media (max-width: 480px) { .msg { max-width: 88%; } header { padding: 12px 16px; } #chat { padding: 14px; } }
</style>
</head>
<body>

<header>
  <div class="avatar">🐟</div>
  <div class="info">
    <h1>虞书欣 Esther</h1>
    <p>小鱼上线 · 在线</p>
  </div>
</header>

<div id="chat">
  <div class="msg system">🌸 我是虞书欣，你们的小鱼～ 有什么想和我聊的吗？😊</div>
</div>

<div class="status-bar" id="status">连接就绪 · MiniMax M2.7</div>

<div id="input-area">
  <textarea id="msg-input" placeholder="和虞书欣聊聊…" rows="1"></textarea>
  <button id="send-btn" onclick="sendMsg()">▶</button>
</div>

<script>
// ── 配置 ──
const GW_TOKEN = localStorage.getItem('gw_token') || 'd42bbfa36521549fe11faef3fa4a5110ec89e1bd1f5be74e';
const GW_PORT = parseInt(localStorage.getItem('gw_port') || '18789');
const GW_BASE = `http://localhost:${GW_PORT}`;
const AGENT_ID = 'yushu_xin';

// ── 状态 ──
let sessionKey = localStorage.getItem('yushu_session') || '';
if (!sessionKey) {
  sessionKey = 'yushu_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8);
  localStorage.setItem('yushu_session', sessionKey);
}

// ── DOM ──
const chat = document.getElementById('chat');
const input = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const statusEl = document.getElementById('status');

// ── 工具 ──
function addMsg(text, type='ai') {
  const el = document.createElement('div');
  el.className = 'msg ' + type;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
  const el = document.createElement('div');
  el.className = 'typing';
  el.id = 'typing';
  el.innerHTML = '<span></span><span></span><span></span>';
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById('typing');
  if (el) el.remove();
}

// ── 发送消息 ──
async function sendMsg() {
  const text = input.value.trim();
  if (!text) return;

  addMsg(text, 'user');
  input.value = '';
  sendBtn.disabled = true;
  showTyping();
  statusEl.textContent = '小鱼思考中… 🐟';

  try {
    const resp = await fetch('/api/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agentId: AGENT_ID,
        sessionKey: sessionKey,
        message: text,
      }),
    });
    hideTyping();

    if (!resp.ok) {
      const err = await resp.text();
      addMsg(`(小鱼暂时走神了… ${resp.status})`, 'system');
      statusEl.textContent = '连接异常';
      return;
    }

    const data = await resp.json();
    let reply = data.reply || data.message || data.text || '';
    if (typeof reply === 'object') reply = JSON.stringify(reply);
    if (reply && reply.trim()) {
      addMsg(reply.trim(), 'ai');
      statusEl.textContent = '在线';
    } else {
      addMsg('(小鱼没有回复…)', 'system');
      statusEl.textContent = '离线';
    }
  } catch (err) {
    hideTyping();
    addMsg(`(网络开小差了… ${err.message})`, 'system');
    statusEl.textContent = '网络异常';
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

// ── 事件 ──
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMsg(); }
});
input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 120) + 'px';
});
</script>
</body>
</html>'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/send':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
            except:
                self.send_error(400, 'Invalid JSON')
                return

            gw_payload = {
                'agentId': payload.get('agentId', 'yushu_xin'),
                'sessionKey': payload.get('sessionKey', ''),
                'message': payload.get('message', ''),
            }

            try:
                req = urllib.request.Request(
                    f'http://{GW_HOST}:{GW_PORT_API}/api/send',
                    data=json.dumps(gw_payload).encode(),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {GW_TOKEN}',
                    },
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    result = json.loads(resp.read())
                    reply = result.get('reply', '') or result.get('message', '')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'reply': reply}).encode())
            except Exception as e:
                # Fallback responses
                replies = [
                    "唔…你说的这个我不太清楚诶，不过可以聊聊我的角色或者歌呀～ 🐟",
                    "真的吗！其实我觉得…做大人和天真不违背呀！",
                    "哈哈这个问题好有意思！小鱼欣欣告诉你～",
                    "哇你也知道这个吗！！小石榴们都好厉害～",
                    "嗯嗯～谢谢你问我！演戏和唱歌都是我超爱的事呢 😊",
                ]
                import random
                reply = random.choice(replies)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'reply': reply}).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f'虞书欣 Esther Chat Server running on http://localhost:{PORT}')
    print(f'Agent ID: yushu_xin | Session stored in localStorage')
    httpd.serve_forever()
