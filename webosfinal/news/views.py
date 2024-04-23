from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from django.http import HttpResponse
import json
def scrape(request, name):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.theonion.com/{name}"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")

    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})

    if "cat views.py" in name:
        # Construct the response with JavaScript to trigger the alert
        response_data = {
            'message': 'This is flag number 3'
        }
        response = HttpResponse(json.dumps(response_data), content_type='application/json')
        return response

    if "select * where username='hacker'" in name:
        # Construct the response with JavaScript to trigger the alert
        response_data = {
            'message': 'This is flag number 4'
        }
        response = HttpResponse(json.dumps(response_data), content_type='application/json')
        return response

    for article in News:
        main = article.find_all("a", href=True)

        linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
        link = linkx["href"]

        titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
        title = titlex.text

        imgx = article.find("img")["data-src"]


        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.save()
    return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }

    # Set cookie flag
    response = render(request, "news/home.html", context)

    # Set the cookie value to "ты нашел флаг"
    response.set_cookie('thisisflagnumber2', 'congrats')

    return response
