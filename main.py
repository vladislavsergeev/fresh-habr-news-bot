import json
import requests
from bs4 import BeautifulSoup

fresh_news = {}
news_dict = {}


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/102.0.5005.63 Safari/537.36 "
    }

    url = "https://habr.com/ru/flows/admin/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all("article", class_="tm-articles-list__item")

    for article in articles_cards:
        article_title = article.find("h2", class_="tm-article-snippet__title tm-article-snippet__title_h2").text.strip()
        article_url = f'https://habr.com{article.find("a", class_="tm-article-snippet__title-link").get("href")}'

        article_date_time = article.find("time").get("title")

        article_id = article_url.split("/")[-2]

        news_dict[article_id] = {
            "article_date_time": article_date_time,
            "article_title": article_title,
            "article_url": article_url
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/102.0.5005.63 Safari/537.36 "
    }

    url = "https://habr.com/ru/flows/admin/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all("article", class_="tm-articles-list__item")

    for article in articles_cards:
        article_url = f'https://habr.com{article.find("a", class_="tm-article-snippet__title-link").get("href")}'
        article_id = article_url.split("/")[-2]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2",
                                         class_="tm-article-snippet__title tm-article-snippet__title_h2").text.strip()

            article_date_time = article.find("time").get("title")

            news_dict[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url,

            }

            fresh_news[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url,

            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    get_first_news()
    check_news_update()


if __name__ == '__main__':
    main()
