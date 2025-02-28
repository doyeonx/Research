import requests
from bs4 import BeautifulSoup
import json
import re

ARCH_LINK = "https://bbs.archlinux.org/"

def get_post_url(post):
    tclcon = post.find('div', class_='tclcon')

    if tclcon:
        a_tag = tclcon.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href = ARCH_LINK + a_tag['href']

    pages = tclcon.find('span', class_='pagestext')
    
    if pages:
        a_tags = pages.find_all('a')
        page_length = len(a_tags)
        return href, page_length
    else:
        return href, None

def get_post_title(post):
    tclcon = post.find('div', class_='tclcon')
    if tclcon:
        a_tag = tclcon.find('a')
        if a_tag:
            title = a_tag.get_text(strip=True)
            return title


# def get_user_data(soup):
#     user = {
#         'username': username,
#         'membership': membership,
#         'registered': registered,
#         'posts': posts,
#     }


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

            comment['order'] = post.find('span', class_='conr')
            comment['time'] = post.find('a').get_text(strip=True)
            comment['user'] = post.find('dt').find('strong').get_text(strip=True)
            comment['content'] = post.find('div', class_='postmsg').text.strip()
            comments.append(comment)

    post_data = {
        'title': post_title,
        'link': post_url,
        'comments': comments,
    }

    return post_data


def get_forum_data(base_url, url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    forum_posts_links = []

    odd_posts_list = soup.find_all('tr', class_='rowodd')
    even_posts_list = soup.find_all('tr', class_='roweven')
    all_posts_list = odd_posts_list + even_posts_list

    for post in all_posts_list:
        # break if there aren't any replies
        reply_num = post.find('td', class_='tc2')

        if reply_num == 0:
            break
        else:
            post_url, page_length = get_post_url(post)
            post_title = get_post_title(post)
            forum_posts_links.append({'url': post_url, 'title': post_title, 'pages': page_length})

    forum_data = []

    for link in forum_posts_links:
        post_data = get_post_data(link['title'], link['url'], link['pages'])
        forum_data.append(post_data)

    return forum_data


def main():
    final_page = 1

    all_forum_data = []

    for i in range(1, final_page + 1):
        url = "https://bbs.archlinux.org/viewforum.php?id=23&p=" + str(i)
        forum_data = get_forum_data(ARCH_LINK, url)
        all_forum_data.append(forum_data)

    print(all_forum_data)

main()
