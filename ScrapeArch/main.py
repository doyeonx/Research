import requests
from bs4 import BeautifulSoup
import json

# Step 1: Send a request to the forum page
url = "https://bbs.archlinux.org/viewtopic.php?id=123456"  # Replace with the actual thread URL
response = requests.get(url)
html_content = response.text

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Find all comments (assuming comments are inside <div class="post"> tags)
comments = []
for post in soup.find_all('div', class_='post'):
    user = post.find('a', class_='username')  # User who posted the comment
    content = post.find('div', class_='content')  # Actual comment content
    if user and content:
        comment = {
            'user': user.text.strip(),
            'content': content.text.strip()
        }
        comments.append(comment)

# Step 4: Save the comments to a JSON file
with open('comments.json', 'w') as json_file:
    json.dump(comments, json_file, indent=4)

print(f"Scraped {len(comments)} comments and saved to 'comments.json'")

