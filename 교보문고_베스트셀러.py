#!/usr/bin/env python
# coding: utf-8

# # 교보문고 문장수집 크롤러

# 장르별 구분 - 소설, 에세이, 시
# 길이
# 작가별

# In[1]:


from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs


import time
import pandas as pd


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# In[174]:


import warnings
warnings.filterwarnings('ignore')


# In[176]:


url = "https://product.kyobobook.co.kr/category/KOR/01#?page=1&type=best&per=50"
# https://product.kyobobook.co.kr/category/KOR/05#?page=1&type=best&per=20
driver = wb.Chrome()
driver.get(url)

books = pd.DataFrame()

for i in range(1,6):
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="homeTabBest"]/div[3]/ol/li['+ str(i) +']/div[2]/div[2]/a/span').click()
    
    soup = bs(driver.page_source, 'lxml')
    title = soup.select('div.auto_overflow_inner > h1 > span')[0].text
    author = soup.select('div.author > a')[0].text
    
    category1 = soup.select('div.intro_book>ul>li>a')[0].text
    category2 = soup.select('div.intro_book>ul>li>a')[1].text
    category3 = soup.select('div.intro_book>ul>li>a')[2].text
    category4 = soup.select('div.intro_book>ul>li>a')[3].text

    killing_list = []
    while True:
        try:
            killing_part = driver.find_elements(By.CSS_SELECTOR,'div.text_killing_part')
            for i in killing_part:
                killing_list.append(i.text)
            driver.find_element(By.XPATH,'//*[@id="scrollSpyProdReview"]/div[3]/div[3]/button[2]').send_keys(Keys.ENTER)
            time.sleep(0.5)
        except:
            break
            

    book_dict = {
        'title':title,
        'author':author,
        'killing_part':killing_list,
        'category1': category1,
        'category2': category2,
        'category3': category3,
        'category4': category4
        
    }
    
    bookAppend = pd.DataFrame(book_dict)
    books = books.append(bookAppend)
    
    driver.back()
books


# In[145]:


books.drop_duplicates('killing_part')

