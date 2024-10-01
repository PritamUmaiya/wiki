from random import choice
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"formTitleInput"}), label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"formTextArea", "style": "height:300px;width:70%;"}), label="Content")


class NewEditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"formTextArea", "style": "height:300px;width:70%;"}), label="Content")

    def __init__(self, title, *args, **kwargs):
        super(NewEditForm, self).__init__(*args, **kwargs)
        entry = util.get_entry(title)
        self.fields['content'].initial = entry

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


def new(request):
    if request.method == "POST":
        form  = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            entries = util.list_entries()

            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/new.html", {
                        "form": form,
                        "error": "Entry already existes!"
                    })

            # Save new entry
            util.save_entry(title, content)

            return HttpResponseRedirect("wiki/" + title)


        else:
            return rneder(request, "encyclopedia/new.html", {
                "form": form
            })

    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewPageForm()
        })


def edit(request, title):
    if request.method == "POST":
        form  = NewPageForm(request.POST)

    else:
        return render(request, "encyclopedia/edit.html", {
            "form": NewEditForm(title)
        })


def random(request):
    random_entry = choice(util.list_entries())
    return HttpResponseRedirect("wiki/" + random_entry)