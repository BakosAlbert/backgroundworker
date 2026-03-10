import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.facebook.com/peter.magyar.102"
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# GitHub Actions cache-ből olvassuk az utolsó posztot
try:
    with open("last_post.txt", "r") as f:
        last_post = f.read().strip()
except:
    last_post = None

def get_latest_post():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href")
        if href and "/posts/" in href:
            return "https://facebook.com" + href
    return None

post = get_latest_post()

if post and post != last_post:
    # Küldés Discordra
    requests.post(WEBHOOK, json={"content": f"🚨 Új Magyar Péter poszt 🚨\n{post}"})

    # Mentés cache-hez
    with open("last_post.txt", "w") as f:
        f.write(post)
