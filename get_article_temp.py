import urllib.request
from bs4 import BeautifulSoup
import re
import time
import pickle
from collections import defaultdict
from tqdm import tqdm
from fake_useragent import UserAgent

# Regular Expressions
find_article_id = re.compile(r'href="/articles/(.+?)" target="_blank">')
find_article_title = re.compile(r'target="_blank"><h3 class="am_card_title" title="(.+?)">')
find_article_category = re.compile(r'<a href="/categories/(.+?)"')
find_article_author_id = re.compile(r'href="/users/(.+?)" target="_blank">')
find_article_author_name = re.compile(r'<div class="avatar_text"><h3>(.+?)</h3>')
find_article_figure = re.compile(r'</path></svg>(.+?)</span>')

def ask_url(url):
    user_agent = UserAgent().random
    head = {"User-Agent": user_agent}
    request = urllib.request.Request(url=url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except Exception as err:
        print(err)
    return html


def get_article_content(article_id):
    url = f'https://www.gcores.com/articles/{article_id}'
    html = ask_url(url)
    soup = BeautifulSoup(html, 'html.parser')

    # 获取所有的story_block
    content_divs = soup.select('div.story_block')

    # 提取所有的内容文本
    content_texts = []
    for div in content_divs:
        content_texts.append(div.get_text(strip=True))

    # 返回所有内容文本
    return '\n'.join(content_texts)


def get_article_data(page_num_start, page_num_end):
    article_data = defaultdict(dict)
    total_articles = (page_num_end - page_num_start) * 12

    for i in tqdm(range(page_num_start, page_num_end), desc="Progress"):
        try:
            url = f'https://www.gcores.com/articles?page={i}'
            html = ask_url(url)
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.find_all("div", class_="am_card_inner"):
                item = str(item)
                article_id = re.findall(find_article_id, item)[0]
                article_title = re.findall(find_article_title, item)[0]
                article_category = re.findall(find_article_category, item)[0]
                author_id = re.findall(find_article_author_id, item)[0]
                author_name = re.findall(find_article_author_name, item)[0]
                figure_list = re.findall(find_article_figure, item)
                if figure_list[0][-1] == 'k':
                    num_likes = int(float(figure_list[0][:-1]) * 1000)
                else:
                    num_likes = int(figure_list[0])
                if figure_list[1][-1] == 'k':
                    num_discussion = int(float(figure_list[1][:-1]) * 1000)
                else:
                    num_discussion = int(figure_list[1])

                # 获取文章内容
                article_content = get_article_content(article_id)

                article_data[article_id] = {
                    'title': article_title,
                    'category': article_category,
                    'author_id': author_id,
                    'author_name': author_name,
                    'likes': num_likes,
                    'discussion_count': num_discussion,
                    'content': article_content  # 添加文章内容
                }

                # 输出当前爬取的文章标题
                print(f"Article Title: {article_title}")

        except Exception as e:
            print(e)

        if i % 10 == 0:
            time.sleep(0.1)

    print("Saving article data...")
    save_pickle(article_data, './data/article_data_with_content')
    return

def save_pickle(data, save_path):
    with open(save_path, 'wb') as save_file:
        pickle.dump(data, save_file)

if __name__ == '__main__':
    get_article_data(1, 2)
