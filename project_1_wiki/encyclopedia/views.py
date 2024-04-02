from django.shortcuts import render, redirect
from markdown2 import markdown
import random 

from . import util


def index(request):
    entries = util.list_entries()
    # Capitalize the first letter of each entry
    entries = [entry.capitalize() for entry in entries]

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    content = util.get_entry(title.strip())

    if content == None:
        content =  markdown("## Page was not found")
    else: 
     content = markdown(content)

    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title})

def search(request):
    query = request.GET.get('q').strip().lower()

    if query in util.list_entries():
        return redirect("entry", title=query)
    
    else: 
        return render(request, "encyclopedia/search.html", {"entries": util.search(query), "q": query})


def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip().lower()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/create.html", {"message": "Field can't be empty.", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {"message": "Title already exist. Try another.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):

    content = util.get_entry(title.strip())

    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()

        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Field can't be empty.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})

def randomPage(request):
    entries = util.list_entries()
    random_index = random.randint(0, len(entries) - 1)  
    random_title = entries[random_index]
    return redirect("entry", title=random_title)