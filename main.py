import bs4
from fake_headers import Headers
import requests

def peak_news(page):
    number_str = 1
    KEYWORDS = ['геймдев',]
    BASEURL = 'https://habr.com'
    while number_str != page+1:
        URLALL = '/ru/all/'
        if number_str == 1:
            URL = f"{BASEURL}{URLALL}"
        else:
            URL = f"{BASEURL}{URLALL}page{number_str}"
        header = Headers(
            browser="chrome",
            os="win",
            headers=True
        ).generate()
        text = requests.get(url=URL, headers=header).text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        posts = soup.find_all(class_='tm-articles-list__item')
        for post in posts:
            title = post.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').text
            for word in KEYWORDS:
                if word in title.split(' '):
                    data = post.find(class_='tm-article-snippet__datetime-published').text
                    href = post.find(class_='tm-article-snippet__title-link').get('href')
                    href = f'{BASEURL}{href}'
                    #parsing only one page
                    description_href = post.find(class_='tm-article-snippet__readmore').get('href')
                    text_one_post = requests.get(url=f'{BASEURL}{description_href}', headers=header).text
                    soup_one_post = bs4.BeautifulSoup(text_one_post, features='html.parser')
                    dirt_description = soup_one_post.find(class_= 'article-formatted-body article-formatted-body article-formatted-body_version-2').text
                    description = dirt_description.split('.')
                    print(f'{data}\n{title}\n{href}\n{dirt_description}\n')
                    for i in description:
                        if i =='':
                            continue
                        print(i.strip(" ") + '.' + '\n')
                else:
                    continue
        number_str += 1
    print('ALL NEWS WERE PARSED')


if __name__ == '__main__':
    input_page = int(input('Введите колличество страниц для изучения: '))
    peak_news(page=input_page)