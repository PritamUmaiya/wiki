from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown

from . import util


def markdown2html(entry):
    markdowner = Markdown()
    return markdowner.convert(entry)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """If the requested entry"""
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2html(entry)
        })
    
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": "Requested entry does not exist!"
        })


def search(request):
    query = request.GET['q']

    entries = util.list_entries()
    results = []

    if query in entries:
        return HttpResponseRedirect("wiki/" + query)

    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })