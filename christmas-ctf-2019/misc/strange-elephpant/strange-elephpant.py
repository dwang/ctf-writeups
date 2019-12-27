#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from PIL import Image
from StringIO import StringIO

rock = Image.open("rock.png")
paper = Image.open("paper.png")
scissors = Image.open("scissors.png")

page = "http://115.68.235.72:12372/index.php"

s = requests.Session()

content = ""

while "XMAS" not in content:
    content = s.get(page).content
    print(content[content.find("</h2><h2>") + len("</h2><h2>"):content.find("</h2><br>")])

    r = s.get("http://115.68.235.72:12372/image.php")
    image = Image.open(StringIO(r.content))

    if list(image.getdata()) == list(rock.getdata()):
        if "어딘가 잘못된 PHP 코끼리를 이겨주세요!" in content: # win
            s.post(page, data={"answer": "보"})
        elif "어딘가 잘못된 PHP 코끼리와 비겨주세요!" in content: # tie
            s.post(page, data={"answer": "바위"})
        elif "어딘가 잘못된 PHP 코끼리에게 져 주세요!" in content: # lose
            s.post(page, data={"answer": "가위"})
    elif list(image.getdata()) == list(paper.getdata()):
        if "어딘가 잘못된 PHP 코끼리를 이겨주세요!" in content: # win
            s.post(page, data={"answer": "가위"})
        elif "어딘가 잘못된 PHP 코끼리와 비겨주세요!" in content: # tie
            s.post(page, data={"answer": "보"})
        elif "어딘가 잘못된 PHP 코끼리에게 져 주세요!" in content: # lose
            s.post(page, data={"answer": "바위"})
    elif list(image.getdata()) == list(scissors.getdata()):
        if "어딘가 잘못된 PHP 코끼리를 이겨주세요!" in content: # win
            s.post(page, data={"answer": "바위"})
        elif "어딘가 잘못된 PHP 코끼리와 비겨주세요!" in content: # tie
            s.post(page, data={"answer": "가위"})
        elif "어딘가 잘못된 PHP 코끼리에게 져 주세요!" in content: # lose
            s.post(page, data={"answer": "보"})

