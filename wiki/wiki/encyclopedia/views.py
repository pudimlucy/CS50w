from django.shortcuts import render
from markdown2 import Markdown
from random import choice

from . import util, forms

# initiates search form
form = forms.searchform()

# MD to HTML conversion
markdowner = Markdown()


def index(request):
    """
    Loads main page, listing all current entries.
    """
    entries = util.list_entries()
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": entries, "form": form},
    )


def page(request, title):
    """
    Loads entry on wiki/[title]
    """
    page = util.get_entry(title)

    # page doesn't exists, renders 404 error
    if not page:
        return render(
            request,
            "encyclopedia/error.html",
            {"error": f"Error 404: page {title} not found"},
        )
    # page exists, renders wiki/[title], converting md to HTML
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": title,
                "content": markdowner.convert(page),
                "form": form,
            },
        )


def get_search(request):
    """
    Gets user's search request and loads results.
    """
    searchform = forms.searchform(request.GET)

    if request.method == "GET":
        # checks for errors and gets search data.
        if searchform.is_valid():
            search = searchform.cleaned_data["search"].lower()
            entries = util.list_entries()

            # runs through all entries and adds matches with search to a list
            matches = [entry for entry in entries if search in entry.lower()]

            if len(matches) == 0:
                # no matches found, renders to 404 error
                return render(
                    request,
                    "encyclopedia/search.html",
                    {"error": "No results found", "form": search},
                )
            elif len(matches) == 1 and matches[0].lower == search:
                # one exact match found, redirects to wiki/[title]
                match = matches[0]
                return page(request, match)
            else:
                # multiple matches found, redirect to search.html
                title = [entry for entry in matches if search == entry.lower()]
                if len(title) > 0:
                    return page(request, title[0])
                else:
                    return render(
                        request,
                        "encyclopedia/search.html",
                        {"results": matches, "form": form},
                    )

        # form not valid, renders error
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": f"Error 105: Invalid Form Data"},
            )

    # invalid request, redirects to main page.
    return index(request)


def new(request):
    """
    Loads page for entry creation and saves entries into memory.
    """

    if request.method == "POST":
        cform = forms.newpageform(request.POST)

        # checks for errors and gets data from form
        if cform.is_valid():
            title = cform.cleaned_data["title"]
            body = cform.cleaned_data["body"]

            # checks if entry title is already used and displays error message
            if util.get_entry(title) != None:
                cform = forms.newpageform()
                return render(
                    request,
                    "encyclopedia/new_page.html",
                    {"form": form, "cform": cform, "error": True},
                )

            # saves entry into memory and redirects to wiki/[title] on new entry.
            util.save_entry(title, body)
            return page(request, title)

        # form not valid, renders error
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": f"Error 105: Invalid Form Data"},
            )

    # renders /new
    else:
        cform = forms.newpageform()
        return render(
            request,
            "encyclopedia/new_page.html",
            {"cform": cform, "form": form, "error": False},
        )


def edit(request):
    """
    Loads page for editing entries and saves alterations into memory.
    """

    # gets entry data
    if request.method == "GET":
        title = request.GET.get("edit")
        eform = forms.editpageform(
            initial={"title": title, "body": util.get_entry(title)}
        )

        # renders /edit
        return render(
            request,
            "encyclopedia/edit_page.html",
            {"title": title, "form": form, "eform": eform},
        )

    # gets entry data
    else:
        title = request.POST.get("edit")
        eform = forms.editpageform(request.POST)

        # checks for error and gets form data
        if eform.is_valid():
            title = eform.cleaned_data["title"]
            content = eform.cleaned_data["body"]

            # saves changes to memory and redirects to wiki/[title]
            util.save_entry(title, content)
            return page(request, title)

        # form not valid, renders error
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error": f"Error 105: Invalid Form Data"},
            )


def random(request):
    """
    Loads random entry page.
    """
    return page(request, choice(util.list_entries()))
