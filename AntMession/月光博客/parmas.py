import feedparser
import os
url = 'https://www.williamlong.info/rss.xml'
d = feedparser.parse(url)
feed = d.feed

last = open('last_published.txt', 'r').read()
if last == feed.published:
        print('not ok')
        os._exit(0)

with open('last_published.txt', 'w') as f:
        f.write(feed.published)

entries = d.entries
len(entries)
# entries[2].title
# entries[2].link
# entries[2].summary
# entries[2]['summary']
content = []
for i in entries:
    tmp = {}
    tmp['title'] = i.title
    tmp['link'] = i.link
    tmp['summary'] = i.summary
    content.append(tmp)
content[1]
# with open('test.md', 'w', encoding='utf-8') as f:
#     for i in content:
#         f.write('- ' + i['title'] + """

# """)
#         f.write(i['link'] + """

# """)
#         f.write(i['summary'] + """

# """)



