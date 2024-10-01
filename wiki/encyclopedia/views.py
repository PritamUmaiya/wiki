from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util


def md2html(content):
    markdowner = Markdown()
    return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """Return the entry if existed"""
    entry = util.get_entry(title)

    if entry is not None:
        # Convert entry to html
        entry = md2html(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
    
    else:
        """Return the apology message"""
        return render(request, "encyclopedia/apology.html", {
            "message": "Entry does not exists!"
        })


def search(request):
    """Return the search result"""
    title = request.GET["q"]
    entries = util.list_entries()

    entries_list = []

    for entry in entries:
        if title == entry:
            return HttpResponseRedirect(reverse("entry", args=[title]))
        elif title.lower() in entry.lower():
            entries_list.append(entry)

    return render(request, "encyclopedia/search.html", {
        "title": title,
        "entries": entries_list
    })