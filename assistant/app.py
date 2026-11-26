"""Minimal Flask API + chat page around the FAQ matcher."""
from flask import Flask, jsonify, render_template_string, request

from .matcher import load

app = Flask(__name__)
matcher = load()

PAGE = """<!doctype html><meta charset=utf-8><title>Assistant demo</title>
<style>body{font-family:system-ui;max-width:560px;margin:2rem auto;padding:0 1rem}
#log div{margin:.4rem 0;padding:.5rem .7rem;border-radius:8px;background:#f2f2f2}
.me{background:#dbeafe!important;text-align:right}small{color:#777}</style>
<h2>FAQ assistant (demo)</h2><div id=log></div>
<form id=f><input id=q style="width:80%" placeholder="Ask something..." autofocus><button>Send</button></form>
<script>
const log=document.getElementById('log');
f.onsubmit=async e=>{e.preventDefault();const t=q.value.trim();if(!t)return;q.value='';
log.insertAdjacentHTML('beforeend','<div class=me></div>');log.lastChild.textContent=t;
const r=await (await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})})).json();
log.insertAdjacentHTML('beforeend','<div></div>');log.lastChild.textContent=r.answer;
log.lastChild.insertAdjacentHTML('beforeend','<br><small>'+r.intent+' · '+r.confidence+' · '+r.language+'</small>');};
</script>"""


@app.get("/")
def index():
    return render_template_string(PAGE)


@app.post("/chat")
def chat():
    message = (request.get_json(silent=True) or {}).get("message", "").strip()
    if not message:
        return jsonify(error="message is required"), 400
    return jsonify(matcher.reply(message[:500]))


if __name__ == "__main__":
    app.run(debug=False, port=5000)
