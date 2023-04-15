from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from markdown2 import Markdown

from . import util

markdownData = Markdown()

class SearchFrom(forms.Form):
    search = forms.CharField(label="search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def gotoTitle(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/wiki.html",{     
        "title": title,
        "data": util.get_entry(title)
    })
    else:
        return render(request, "encyclopedia/wiki.html",{     
            "title": title,
            "data": markdownData.convert(util.get_entry(title))
        })

def search(request):
    try:
        title = request.GET['q'].lower()
    except:
        title = "NULL"
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/wiki.html",{     
            "title": title,
            "data": markdownData.convert(util.get_entry(title))
        })
    else:
        searchList = []
        noResult = True
        for item in util.list_entries():
            if title in item.lower():
                searchList.append(item)
                noResult = False
        
        return render(request, "encyclopedia/search.html",{
            "title": title,
            "noResult": noResult,
            "searchList": searchList
        })

def create(request):
    return render(request, "encyclopedia/create.html")