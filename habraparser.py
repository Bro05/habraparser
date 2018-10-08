# -*- coding: utf-8 -*-

import urllib.request as req
from bs4 import BeautifulSoup

article_block = {"name": "li", "class": "content-list__item"}
ini = [{"name": "Заголовок", "pattern": {"name": "h2", "class": "post__title"}},
       {"name": "Автор", "pattern": {"name": "span", "attrs": {"class": "user-info__nickname"}}},
       {"name": "Теги", "pattern": {"name": "a", "attrs": {"class": "hub-link"}}, "istags": True},
       {"name": "Описание", "pattern": {"name": "div", "attrs": {"class": "post__text"}}},
       {"name": "Комментарии", "pattern": {
           "counter": {"name": "span", "class": "post-stats__comments-count"},
           "postlink": {"name": "a", "class": "post__title_link"},
           "comment": {"name": "div", "class": "comment__message"},
           },
        "iscomments": True,
        },
       ]


def get_data(data, name, pattern, iscomments=False, istags=False):
    if istags:
        result = ", ".join([tag.text.strip() for tag in data.find_all(**pattern)])
    elif iscomments:
        if not data.find(**pattern["counter"]):
            return ""
        else:
            postlink = data.find(**pattern["postlink"])["href"]
            with req.urlopen(postlink) as comments_data:
                comments_data = BeautifulSoup(comments_data.read(), "lxml")
                return get_data(comments_data, name, pattern["comment"])
    else:
        data = data.find(**pattern)
        if data:
            result = data.text.strip()
        else:
            return None
    return "{}: {}".format(name, result)


if __name__ == "__main__":

    with req.urlopen("https://habr.com/") as response:
        i = 0
        limit = 100
        articles = BeautifulSoup(response.read(), "lxml").find_all(**article_block)
        for a in articles:
            if i == 10 or limit == 0:
                break
            head = get_data(data=a, **ini[0])
            if not head:
                pass
            else:
                print(head)
                for item in ini[1:]:
                    print(get_data(data=a, **item))
                print("\n")
                i += 1
                limit -= 1
