from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    page = util.get_entry(title)
    
    if not page:
        return render(request,"encyclopedia/error.html") 
    else:
        return render(request,"encyclopedia/entry.html",{
        'title': title, 
        'content': page,
    })