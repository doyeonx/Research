import sys
sys.path.insert(1, '../')
import files
import requests
from bs4 import BeautifulSoup
import json
import re
import time

ARCH_LINK = "https://bbs.archlinux.org/"

def get_post_url(post):
    tclcon = post.find('div', class_='tclcon')

    if tclcon:
        a_tag = tclcon.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href = ARCH_LINK + a_tag['href']

    pages = tclcon.find('span', class_='pagestext')
    
    if href and pages:
        a_tags = pages.find_all('a')
        page_length = len(a_tags)
        return href, page_length
    elif href:
        return href, None
    else:
        return

def get_post_title(post):
    tclcon = post.find('div', class_='tclcon')
    if tclcon:
        a_tag = tclcon.find('a')
        if a_tag:
            title = a_tag.get_text(strip=True)
            return title

def get_post_data(post_title, post_url, page_length):
    if not page_length:
        page_length = 1
    
    comments = []
    for i in range(1, page_length + 1):
        url = post_url + "&p=" + str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        blockposts = soup.find_all('div', class_='blockpost')
        for post in blockposts:
            comment = {}

            if post and 'id' in post.attrs:
                comment['id'] = post['id']

            conr_span = post.find('span', class_='conr')
            comment['order'] = conr_span.get_text(strip=True) if conr_span else None

            time_a = post.find('a')
            comment['time'] = time_a.get_text(strip=True) if time_a else None

            user_strong = post.find('dt').find('strong')
            comment['user'] = user_strong.get_text(strip=True) if user_strong else None

            postmsg_div = post.find('div', class_='postmsg')
            comment['content'] = postmsg_div.get_text(strip=True) if postmsg_div else None

            comments.append(comment)

    post_data = {
        'title': post_title,
        'link': post_url,
        'comments': comments,
    }

    return post_data

def get_forum_data(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    forum_posts_links = []

    odd_posts_list = soup.find_all('tr', class_='rowodd')
    even_posts_list = soup.find_all('tr', class_='roweven')
    all_posts_list = odd_posts_list + even_posts_list

    for post in all_posts_list:
        if 'sticky' in post.get('class', []):
            continue

        reply_num_td = post.find('td', class_='tc2')
        if reply_num_td:
            reply_num = reply_num_td.get_text(strip=True)
            if reply_num == 0:
                continue
        
        post_url, page_length = get_post_url(post)
        post_title = get_post_title(post)
        forum_posts_links.append({'url': post_url, 'title': post_title, 'pages': page_length})

    forum_data = []

    for link in forum_posts_links:
        post_data = get_post_data(link['title'], link['url'], link['pages'])
        forum_data.append(post_data)

    return forum_data

def main():
    json_files = files.JSON_FILES
    
    for i in range(len(json_files)):
        file_name = json_files[i]['file_name']
        start_page = json_files[i]['start_page']
        final_page = json_files[i]['final_page']

        print(f"file: {file_name}")

        all_forum_data = []

        for i in range(start_page, final_page):
            print(i)
            url = "https://bbs.archlinux.org/viewforum.php?id=23&p=" + str(i)
            forum_data = get_forum_data(url)
            all_forum_data.extend(forum_data)

            with open("temp.json", 'w') as json_file:
                json.dump(all_forum_data, json_file, indent=4)

main()
