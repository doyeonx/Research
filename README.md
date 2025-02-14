# AP Research Project

### Step 1: Collect data from the [Arch Linux Community Forum](https://bbs.archlinux.org/viewforum.php?id=23)
#### 1.1 WebScrape
Use [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to collect 7 types of data:
1. ID of the Post
2. Order of the comment
3. Time of comment
4. Comment
5. Username of commenter
6. User's registered date
7. User's number of posts

#### 1.2 Store User Data
Use the username as the primary key to determine the types of users in step 4.

### Step 2: Classify Toxic Comments
From the data collected in step 1, we can use the comment themselves and the context of the comment generated through [BERT](https://huggingface.co/docs/transformers/en/model_doc/bert) to generate a toxicity score also using BERT.

### Step 3: Divide Toxic Comments into Themes
