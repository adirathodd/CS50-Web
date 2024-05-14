from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        entryName = request.POST['entry']
        content = request.POST['content']

        if util.get_entry(entryName) is not None:
            return render(request, "encyclopedia/error.html", {
                'message': "This page already exists"
            })
        else:
            util.save_entry(entryName, content)
            return render(request, "encyclopedia/title.html", {
            "title": entryName,
            "content": convertor(entryName)
            })


def convertor(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def edit(request):
    if request.method == "GET":
        entry = request.GET['entry']
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            'title': entry,
            'content': content
        })
    elif request.method == "POST":
        entry = request.POST['entry']
        content = request.POST['content']
        util.save_entry(entry, content)
        return render(request, "encyclopedia/title.html", {
            "title": entry,
            "content": convertor(entry)
        })
def get_page(request, title):
    content = convertor(title)
    if content == None:
        return render(request, 'encyclopedia/error.html', {
            'message': "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content
        })
    

def searchEntry(request):
    if request.method == "POST":
        entry = request.POST['q']
        content = convertor(entry)
        if content != None:
            return render(request, "encyclopedia/title.html", {
            "title": entry,
            "content": content
        })
        else:
            totalEntries = util.list_entries()
            possibilities = []
            for entry1 in totalEntries:
                if entry.upper() in entry1.upper():
                    possibilities.append(entry1)
            return render(request, "encyclopedia/search.html", {
                "possibilities": possibilities
            })
        
def random(request):
    totalEntries = util.list_entries()
    randomEntry = choice(totalEntries)
    return render(request, "encyclopedia/random.html", {
        "title": randomEntry,
        "content": convertor(randomEntry)
    })
