import requests
from bs4 import BeautifulSoup
import json
import re

def get_forum_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    forum_data = []

    # Find all posts
    posts = soup.find_all('div', class_='blockpost')
    for post in posts:
        post_data = {}
        
        # Get ID
        post_data['ID'] = post['id']
        
        # Get Order
        order_tag = post.find('span', class_='conr')
        post_data['Order'] = order_tag.text if order_tag else None
        
        # Get Username
        username_tag = post.find('dt').find('strong')
        post_data['Username'] = username_tag.text if username_tag else None
        
        # Get Time
        time_tag = post.find('a', href=re.compile(r'viewtopic\.php\?pid=\d+#p\d+'))
        post_data['Time'] = time_tag.text if time_tag else None
        
        # Get Post Content
        content_tag = post.find('div', class_='postmsg')
        post_data['Content'] = content_tag.text.strip() if content_tag else None
        
        forum_data.append(post_data)
    
    return forum_data

def get_all_pages(start_url):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the breadcrumb for pagination
    breadcrum = soup.find('div', class_='linkst')
    if not breadcrum:
        return [start_url]
    
    # Extract the last page number
    last_page_link = breadcrum.find_all('a')[-1]['href']
    last_page_number = int(re.search(r'&p=(\d+)', last_page_link).group(1))
    
    # Generate all page URLs
    base_url = start_url.split('&p=')[0]
    all_pages = [f"{base_url}&p={page_num}" for page_num in range(1, last_page_number + 1)]
    
    return all_pages

def main():
    start_url = 'https://bbs.archlinux.org/viewtopic.php?id=273933'  # Example forum thread URL
    all_pages = get_all_pages(start_url)
    
    all_forum_data = []
    for page_url in all_pages:
        forum_data = get_forum_data(page_url)
        all_forum_data.extend(forum_data)
    
    # Save to JSON file
    with open('forum_data.json', 'w') as f:
        json.dump(all_forum_data, f, indent=4)

if __name__ == "__main__":
    main()