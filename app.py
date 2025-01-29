from dotenv import load_dotenv
from fastapi import FastAPI,  Response,  Request, Body, Form
from fastapi.responses import FileResponse
from profile_summarizer import get_profile_with
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Annotated
import json

import uvicorn  

load_dotenv()

app = FastAPI(
    title="generate-profile-service",
    description=f"service to generate linkedin profile summary",
    version="0.0.1"
)


templates = Jinja2Templates(directory="/templates")

## for loading static html files
app.mount('/get_profile_summary', StaticFiles(directory='templates', html=True))

templates = Jinja2Templates(directory='templates')

@app.post("/process", status_code=200)
async def generate_profile_summary(name: str=Form(...)):
    #name= Request.form["name"]
    summary, profile_pic_url= get_profile_with(name= name)

    return {"summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url
            }


    # return jsonify
    # #return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, World!"})
    # #return templates.TemplateResponse("index.html")
    # return templates.render_unicode('index.html')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')