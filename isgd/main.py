import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class Url(BaseModel):
    url: str

url_shorturl = 'https://is.gd/create.php'
headers = {
    'authority': 'is.gd',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.6',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'recent=0KkhTq',
    'origin': 'https://is.gd',
    'referer': 'https://is.gd/index.php',
    'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

@app.post('/new')
def new_url(url: Url):
    if url.url == '':
        return {'error': 'No valid URL provided'}
    data = {
      'url': url.url,
      'shorturl': '',
      'opt': '0'
    }
    response = requests.post(url_shorturl, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    url_short = soup.find('input', {'id': 'short_url'})['value']
    return url_short