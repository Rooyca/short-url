import requests, os
import urllib.parse

from fastapi import FastAPI, Request
from dotenv import load_dotenv
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

repository_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
repository_name = os.getenv("GITHUB_REPOSITORY_NAME")
access_token = os.getenv("GITHUB_ACCESS_TOKEN")
url_shortener = os.getenv("URL_SHORTENER")

class Item(BaseModel):
    url: str

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", { 
            "request": request, 
            "title": "GHUS 🔥",
            "description": "Make your url shorter using GitHub issues. ",
            "author": "rooyca",
            "keywords": "fastapi, python, api, github, url, shortener, htmx, bootstrap",
            "icon": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0iIzAwMDAwMCIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGQ9Ik0yNCwxMjhhNDAsNDAsMCwwLDAsNDAsNDBoNDBhOCw4LDAsMCwxLDAsMTZINjRBNTYsNTYsMCwwLDEsNjQsNzJoNDBhOCw4LDAsMCwxLDAsMTZINjRBNDAsNDAsMCwwLDAsMjQsMTI4Wk0xOTIsNzJIMTUyYTgsOCwwLDAsMCwwLDE2aDQwYTQwLDQwLDAsMCwxLDAsODBIMTUyYTgsOCwwLDAsMCwwLDE2aDQwYTU2LDU2LDAsMCwwLDAtMTEyWiI+PC9wYXRoPjwvc3ZnPg=="
            })

@app.post("/api/short")
async def short(request: Request):
    data = await request.body()
    data_str = data.decode()
    url_parse = urllib.parse.unquote(data_str)
    url = url_parse.split("=")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "title": "=".join(url[1:]),
        "body": ""
    }

    response = requests.post(f"https://api.github.com/repos/{repository_owner}/{repository_name}/issues", 
                                headers=headers, json=payload)

    if response.status_code == 201:
        return templates.TemplateResponse("display_url.html", {
            "request": request,
            "description": "Your url is ready! Make sure to copy it before you leave this page.",
            "url": url_shortener+str(response.json()['number']),
            })
    else:
        return {"error": "fail", "message": response.json()["message"]}
    return