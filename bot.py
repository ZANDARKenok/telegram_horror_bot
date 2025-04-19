import requests
import random
import os
import time
import html

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

HEADERS = {'User-Agent': 'Mozilla/5.0'}
REDDIT_URL = 'https://www.reddit.com/r/shortscarystories/top.json?limit=50&t=day'

def get_random_story():
    try:
        response = requests.get(REDDIT_URL, headers=HEADERS)
        posts = response.json()['data']['children']
        post = random.choice(posts)['data']
        title = html.unescape(post['title'])
        story = html.unescape(post['selftext'])
        return f"👻 *{title}*\n\n{story}"
    except Exception as e:
        print(f"[Ошибка] {e}")
        return None

def get_random_image():
    folder = os.path.join(os.path.dirname(__file__), "images")
    images = [f for f in os.listdir(folder) if f.endswith((".jpg", ".png"))]
    return os.path.join(folder, random.choice(images)) if images else None


def send_post(text, image_path):
    with open(image_path, 'rb') as img:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
        data = {
            'chat_id': CHANNEL_USERNAME,
            'caption': text,
            'parse_mode': 'Markdown'
        }
        files = {'photo': img}
        r = requests.post(url, data=data, files=files)
        print(f"[Отправлено] Статус: {r.status_code}")

while True:
    story = get_random_story()
    img = get_random_image()
    if story and img:
        send_post(story, img)
    else:
        print("Пропуск...")
    time.sleep(2700)  # 45 минут
