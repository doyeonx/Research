# AP Research Project

### Step 1: Collect data from the [Arch Linux Community Forum](https://bbs.archlinux.org/viewforum.php?id=23)
#### 1.1 WebScrape
Use [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to collect 7 types of data:
4. Comment
5. Username of commenter
6. User's registered date
7. User's number of posts

1. ID of the Post
```html
<div id="p2225074" class="blockpost rowodd firstpost blockpost1">
```

2. Order of the comment
```html
<span class="conr">#1</span>
```

3. Username postleft
```html
<dt><strong>LeonN</strong></dt>
```

4. Time
```html
<a href="viewtopic.php?pid=2225074#p2225074">2025-02-07 07:48:41</a>
```

5.  postleft
```html

					<h3>Alacritty terminal won't start on xfce fresh install</h3>
					<div class="postmsg">
						<div class="codebox"><pre><p>I'm on a fresh Arch linux installation with xfce. I installed Alacritty to use it as main terminal, but it won't appear on screen. I say only appear because Alacritty is indeed starting. </p><code>[leo@LeoLaptop ~]$ ps aux | grep "alacritty"
leo          979  0.3  0.2 793340 63432 ?        Sl   02:31   0:03 alacritty
leo         2489  0.4  0.5 790512 127072 ?       Sl   02:35   0:02 alacritty
leo         4880  0.0  0.0  10244  6252 pts/0    S+   02:46   0:00 grep --color=auto alacritty</code></pre></div><p>When I run it from the xfce terminal, i get no output, just the process running as if alacritty appeared on the screen.</p>
					</div>
```

6. Registered postleft
```html
<dd><span>Registered: 2022-12-19</span></dd>
```

7. Post number postleft
```html
<dd><span>Posts: 82</span></dd>
```


#### 1.2 Store User Data
Use the username as the primary key to determine the types of users in step 4.

### Step 2: Classify Toxic Comments
From the data collected in step 1, we can use the comment themselves and the context of the comment generated through [BERT](https://huggingface.co/docs/transformers/en/model_doc/bert) to generate a toxicity score also using BERT.

### Step 3: Divide Toxic Comments into Themes
