import requests
import os
from lxml import etree


session = requests.Session()
session.headers = {
    "Content-Type": "text/html",
    "Vary": "Accept-Encoding",
    "Last-Modified": "Tue, 28 Sep 2021 05:57:45 GMT",
    "Vary": "Accept-Encoding",
    "ETag": "W/\"6152aed9-715a",
    "Server": "cdn",
    "X-Cache-Status": "HIT",
    "Content-Encoding": "gzip"
}

"""
for f in *.md;do `sed -i 's/^\t*\([a-z-]*\)（1/* \1（1/g' "$f"`;done
for f in *.md;do `sed -i 's/^\([a-z-]*\)（1/* \1（1/g' "$f"`;done
for f in *.md;do `sed -i 's/^\([a-z-]*\)(1/* \1（1/g' "$f"`;done
for f in *.md;do `sed -i 's/^\t*\([a-z-]*\) (1/* \1（1/g' "$f"`;done
for f in *.md;do `sed -i 's/^\t*\([a-z-]*\)(1/* \1（1/g' "$f"`;done
for f in *.md;do `sed -i 's/^\t*\([0-9]*\) \([a-zA-Z]\)/\1. \2/g' "$f"`;done
"""


def get_article(url, title):
    resp = session.get("https:"+url, timeout=10)
    content = resp.content.decode("utf-8")
    selector = etree.HTML(content)

    fname = title.replace(" ", "-")
    f = open("./nce4/"+fname+".md", "w", encoding="utf-8")
    f.write("# " + title + "\n")
    items = selector.xpath('//div[@class="content"]/p[./audio]/following-sibling::*')
    for item in items[1:]:
        c = item.xpath("string()").strip()
        if c.lower() in ["notes on the text 课文注释", "参考译文", "new words and expressions 生词和短语"]:
            c = "### " + c
        f.write(c)
        f.write("\n\n")
    f.close()


def get_chapters():
    # https://web.archive.org/web/20230926202149/http://en-nce.xiao84.com/nce4/20293.html
    urls = [f"https://en-nce.xiao84.com/nce4/p1_{i}.html" for i in range(1, 3)]
    for url in urls:
        resp = session.get(url, timeout=10)
        selector = etree.HTML(resp.content.decode("utf-8"))
        items = selector.xpath('//div[@class="if0"]/ul/li')
        for item in items:
            article_url = item.xpath("./h3/a/@href")
            if len(article_url) == 0:
                continue
            article_title = item.xpath("./h3/a/text()")
            get_article(article_url[0], article_title[0])


if __name__ == "__main__":
    get_chapters()
