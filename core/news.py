from bs4 import BeautifulSoup
import requests
from core.config import URL, DOMEN, HEADERS
import json

def get_html(url, headers=HEADERS):
    response = requests.get(url=URL, headers=HEADERS)
    src = response.text
    return src


def get_response(response):
    soup = BeautifulSoup(response, "html.parser")

    news = soup.find_all("div", class_="tn-news-author-list-item")
    teg_image = soup.find_all("div", class_="tn-image-container")

    news_info = []
    for item in news:
        try:
            title = item.find("div", class_="tn-news-author-list-item-text").find("span", class_="tn-news-author-list-title")
            description = item.find("div", class_="tn-news-author-list-item-text").find("p", class_="tn-announce")
            date_time = item.find("div", class_="tn-news-author-list-item-text").find("li")
            news_url = DOMEN + item.find("a").get("href")
            image = item.find("div", class_="tn-image-container").find("img").get("src")
        except:
            image = item.find("div", class_="tn-video-container").find("source").get("src")
            information = {
            "title": title.text,
            "description": description.text,
            "date_time": date_time.text.strip(),
            "image": DOMEN + image,
            "url": news_url
        }
        else:
            information = {
            "title": title.text,
            "description": description.text,
            "date_time": date_time.text.strip(),
            "image": DOMEN + image,
            "url": news_url
        }

        news_info.append(information)
    return news_info


def NewsAlmatyParser():
    response = get_html(url=URL)
    soup = get_response(response)
    
    with open(f"core/json/news_almaty.json", "w", encoding="utf-8") as file:
        json.dump(soup, file, indent=4, ensure_ascii=False)