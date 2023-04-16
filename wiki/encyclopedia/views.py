from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

import random

from . import util

markdownData = Markdown()

class AddForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name':'title','placeholder':'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Content, use Markdown please.'}))
    
class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Content, use Markdown please.'}))
    
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
    if request.method == "POST":
        form = AddForm(request.POST)
        currentList = util.list_entries()
        
        if form.is_valid():
            
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            for item in currentList:
                if title.lower() == item.lower():
                    # ERROR
                    return render(request, "encyclopedia/create.html",{
                    "form": form,
                    "errorMsg": f"There is already a title called \"{item}\"."
                    })
                    
                    
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("gotoTitle", args=[title]))
    else:
        return render(request, "encyclopedia/create.html",{
            "form": AddForm()
        })
        
def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)   
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("gotoTitle", args=[title]))
    
    else:
        newForm = EditForm()
        if util.get_entry(title) != None:
            newForm.initial['content'] = util.get_entry(title)
            return render(request, "encyclopedia/edit.html",{
                "form": newForm,
                "title": title
            })
        else:
            return HttpResponseRedirect(reverse("gotoTitle", args=[title]))
 
def randomWiki(request):
     dataList = []
     for item in util.list_entries():
         dataList.append(item)
         
     title = random.choice(dataList)
     return HttpResponseRedirect(reverse("gotoTitle", args=[title]))
     
      
