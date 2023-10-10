from django.shortcuts import render, redirect
from django import forms
import markdown2
from random import choice

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter title", "class": "form-control"}
        ),
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter the Markdown content for the page",
                "class": "form-control",
            }
        ),
    )


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})


def entry(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/404.html")

    html_content = markdown2.markdown(entry)
    return render(
        request, "encyclopedia/entry.html", {
            "title": title, "content": html_content}
    )


def random(request):
    random_entry = choice(util.list_entries())
    return redirect("encyclopedia:entry", title=random_entry)


def search(request):
    query = request.POST.get("q", "").strip().lower()
    entries = util.list_entries()
    results = [entry for entry in entries if query in entry.lower()]

    if not len(results):
        return render(request, "encyclopedia/404.html")
    elif len(results) == 1 and results[0].lower() == query:
        return redirect("encyclopedia:entry", title=query)
    else:
        return render(request, "encyclopedia/search_results.html", {"entries": results})


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) is not None:
                return render(
                    request,
                    "encyclopedia/error.html",
                    {"error": "Entry already exists with the provided title"},
                )
            else:
                util.save_entry(title, content)
                return redirect("encyclopedia:entry", title=title)
    else:
        form = NewEntryForm()

    return render(request, "encyclopedia/create.html", {"form": form})


def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", title=title)
    else:
        entry_content = util.get_entry(title)
        form = NewEntryForm(initial={"title": title, "content": entry_content})
        return render(request, "encyclopedia/edit.html", {"title": title, "form": form})


def delete(request, title):
    util.delete_entry(title)
    return redirect("encyclopedia:index")
