from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
from random import choice

from . import util


class NewEntryFrom(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={'placeholder': "Enter title",'class': 'form-control'})
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'placeholder': "Enter the Markdown content for the page",'class': 'form-control'})
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/404.html")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(entry)
    })


def random(request):
    random_entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[random_entry]))


def search(request):
    query = request.POST.get("q").strip().lower()

    entries = util.list_entries()
    results = []

    for entry in entries:
        entry = entry.lower()

        if (query == entry):
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
        elif query in entry:
            results.append(entry)

    if results:
        return render(request, "encyclopedia/found.html", {
            "entries": results
        })
    else:
        return render(request, "encyclopedia/404.html")


def create(request):
    if request.method == "POST":
        form = NewEntryFrom(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/error.html", {
                        "error": "Entry already exists with the provided title"
                    })

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryFrom()
        })


def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })


def delete(_, title):
    util.delete_entry(title)
    return HttpResponseRedirect(reverse("encyclopedia:index"))
