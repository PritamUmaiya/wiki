from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


class NewContentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


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


def new(request):
    """Add new page"""
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if entry already exists
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/new.html", {
                    "message": "Entry already exists!",
                    "form": form
                })
            
            else:
                # Save new entry
                util.save_entry(title, content)

                # Redirect to the new entry page
                return HttpResponseRedirect(reverse("entry", args=[title]))

        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewPageForm()
        })


def edit(request, title):
    """Edit the entry"""
    if request.method == "POST":
        form = NewContentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            # Save the content
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('entry', args=[title]))
        
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    
    else:
        initial_data = {
            'content': util.get_entry(title)
        }

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": NewContentForm(initial=initial_data)
        })