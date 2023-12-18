# -*- coding: utf-8 -*-            
# @Author : Zhicheng_Zhang
# @Time : 12/19/2023 12:05 AM
import pickle
from pprint import pprint

# 读取pickle文件
with open('./data/article_data_with_content', 'rb') as file:
    article_data = pickle.load(file)

# # 打印读取的数据
pprint(article_data)

#打印标题
# article_id_to_check = 'your_article_id'
#
# if article_id_to_check in article_data:
#     title_of_article = article_data[article_id_to_check]['title']
#     print(f"Title of the article with ID {article_id_to_check}: {title_of_article}")
# else:
#     print(f"Article with ID {article_id_to_check} not found.")

#打印内容
# title_to_check = '2024 年机核招聘开启！'
#
# # 在article_data字典中查找标题
# matching_articles = [article_id for article_id, article_info in article_data.items() if article_info['title'] == title_to_check]
#
# # 打印匹配的文章内容
# for article_id in matching_articles:
#     print(f"Article ID: {article_id}")
#     print(f"Title: {title_to_check}")
#     print(f"Content:\n{article_data[article_id]['content']}\n")
