from django.shortcuts import render

from . import util, forms


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def page(request, title):
    page = util.get_entry(title)

    if not page:
        return render(request, "encyclopedia/error.html")
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": title,
                "content": page,
            },
        )


def get_search(request, q):
    searchform = forms.searchform(request.GET)

    if request.method == "GET":

        if searchform.is_valid():
            search = searchform.cleaned_data["search"].lower()
            entries = util.list_entries()

            # runs through all entries and adds matches with search to a list
            matches = [entry for entry in entries if search in entry.lower()]

            if len(matches) == 0:
                # no matches found, loads 404 error
                # TODO: display search.html with error message
                return render(request, "encyclopedia/error.html")
            elif len(matches) == 1 and matches[0].lower == search:
                # one exact match found, loads wiki/[title]
                return page(request, matches[0])
            else:
                # TODO: multiple matches found, redirect to search.html
                return index(request)

    # Invalid request, loads index.
    return index(request)
