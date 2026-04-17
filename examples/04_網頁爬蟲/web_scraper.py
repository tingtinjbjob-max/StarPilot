#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
網頁爬蟲 - 抓取 i23.uk 的文章標題和內容
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def scrape_articles(url, num_articles=3):
    """
    抓取網頁上的文章標題和內容

    Args:
        url: 網頁 URL
        num_articles: 要抓取的文章數量

    Returns:
        articles: 文章列表，每篇包含 title 和 content
    """

    try:
        # 設定 User-Agent 模擬瀏覽器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        print(f"正在訪問 {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()

        # 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []

        # 查找文章容器 - 嘗試常見的 CSS 選擇器
        article_containers = soup.find_all('article')
        if not article_containers:
            article_containers = soup.find_all(
                class_=['post', 'article', 'entry', 'item'])
        if not article_containers:
            article_containers = soup.find_all(
                'div', class_=lambda x: x and 'article' in x.lower())

        print(f"找到 {len(article_containers)} 個文章容器")

        for idx, article in enumerate(article_containers[:num_articles]):
            # 抓取標題 - 從 entry-header 裡的 h1 或 h2
            title = None
            header = article.find('header', class_='entry-header')
            if header:
                for tag in ['h1', 'h2', 'h3', 'h4']:
                    title_elem = header.find(tag)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        break

            # 如果 header 裡找不到，就找整個 article 裡的第一個標題
            if not title:
                for tag in ['h1', 'h2', 'h3', 'h4']:
                    title_elem = article.find(tag)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        break

            # 抓取內容 - 從 entry-content div
            content = None
            content_elem = article.find('div', class_='entry-content')
            if content_elem:
                content = content_elem.get_text(strip=True)

            # 如果沒找到 entry-content，就找所有段落
            if not content:
                content_elems = article.find_all('p')
                if content_elems:
                    content = ' '.join([p.get_text(strip=True)
                                       for p in content_elems[:3]])

            if title or content:
                articles.append({
                    'title': title or '（無標題）',
                    'content': content or '（無內容）'
                })
                print(f"✓ 已抓取第 {idx+1} 篇: {(title or '無標題')[:50]}...")

        return articles

    except requests.exceptions.RequestException as e:
        print(f"❌ 錯誤: {e}")
        return []


def save_to_txt(articles, filename):
    """
    將文章儲存為 TXT 檔案

    Args:
        articles: 文章列表
        filename: 輸出檔案名稱
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"網頁爬蟲結果\n")
            f.write(f"URL: https://www.i23.uk/\n")
            f.write(f"抓取時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            for idx, article in enumerate(articles, 1):
                f.write(f"【第 {idx} 篇】\n")
                f.write(f"標題: {article['title']}\n")
                f.write(f"內容: {article['content']}\n")
                f.write("-" * 80 + "\n\n")

        print(f"✓ 已儲存到 {filename}")
        return True

    except Exception as e:
        print(f"❌ 儲存錯誤: {e}")
        return False


if __name__ == '__main__':
    url = 'https://www.i23.uk/'

    # 抓取前三篇文章
    articles = scrape_articles(url, num_articles=3)

    if articles:
        # 儲存為 TXT 檔案
        filename = f'i23_articles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        save_to_txt(articles, filename)
    else:
        print("❌ 未能抓取任何文章")
