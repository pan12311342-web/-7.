from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from .pipeline import process

app = FastAPI(title="PR7 Invoice Analyzer")

HTML = '''<!doctype html><html lang="uk"><head><meta charset="utf-8">
<title>PR7 — Аналіз рахунку</title><style>
body{font-family:Arial;max-width:900px;margin:40px auto;padding:0 20px}
.card{border:1px solid #ddd;border-radius:12px;padding:20px;margin:15px 0}
pre{white-space:pre-wrap;background:#f6f6f6;padding:15px;border-radius:8px}
button{padding:10px 18px}</style></head><body>
<h1>Практична робота №7</h1><p>Мультимодальний аналіз рахунку</p>
<div class="card"><form action="/analyze" method="post" enctype="multipart/form-data">
<input type="file" name="file" accept="image/*" required><button>Проаналізувати</button>
</form></div></body></html>'''

@app.get("/", response_class=HTMLResponse)
def home(): return HTML

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile=File(...)):
    try:
        data=await file.read()
        result=process(data)
        return HTMLResponse("<h1>Результат</h1><h2>Рішення: %s</h2><div class='card'><b>Проблеми:</b><pre>%s</pre></div><div class='card'><pre>%s</pre></div><a href='/'>Назад</a>" %
            (result["decision"], "\n".join(result["problems"]) or "Немає", __import__("json").dumps(result,ensure_ascii=False,indent=2)))
    except Exception as e:
        return HTMLResponse(f"<h1>Помилка обробки</h1><p>{e}</p><a href='/'>Назад</a>", status_code=400)
