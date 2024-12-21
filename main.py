import requests, json, os
from bs4 import BeautifulSoup
from fake_headers import Headers

KEYWORDS = ["дизайн", "фото", "web", "python"]
headers = Headers("chrome", "win")
url = "https://habr.com"


def find_article(page, keywords: list):
    """
    Поиск статей по ключевым словам, с последующим сохранением в словарь.
    Принимает в себя номер текущей страницы и ключевые слова.
    """
    if page == 0:
        request = requests.get(f"{url}/ru/articles/", headers=headers.generate())
    else:
        request = requests.get(f"{url}/ru/articles/page{page}", headers=headers.generate())

    soup = BeautifulSoup(request.content, "html.parser")

    res = dict()
    articles = soup.find_all("article", class_="tm-articles-list__item")
    for article in articles:
        tags = [tag.text.lower() for tag in article.find_all("span", class_="tm-publication-hub__link-container")]
        match_list = list()

        for tag in tags:
            for kw in keywords:
                if kw.lower().strip() in tag.lower().strip():
                    match_list.append(tag)
        if match_list:
            title = article.find('a', class_='tm-title__link').text
            time = article.find('time')['title']
            href = url + article.find('a', class_='tm-title__link')['href']
            description = article.find('div', class_='article-formatted-body').text

            res[title] = {'time': time, 'href': href, 'description': description}
            page += 1
    return page, res


def search_pages(limit: int, keywords: list):
    """
    Сканирование страниц по ключевым словам.
    Принимает в себя лимит на количество сканирований страниц и ключевые слова.
    """
    page = 0
    links = dict()
    print('Ищем подходящие статьи...')
    for num in range(limit):
        print(f'Идет процесс поиска: {num + 1}')
        page, res = find_article(page, keywords)
        links.update(res)
    print(f'\nПоиск завершен.\n')
    return links


result = search_pages(40, KEYWORDS)

# Выводим в консоль подходящие статьи в нужном формате.
for header, dict_ in result.items():
    result_search = f"{dict_['time']} – {header} – {dict_['href']}"
    print(result_search)

# Сохраняем данные в json
with open(f'{os.getcwd()}/Articles.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, indent=2, ensure_ascii=False))
