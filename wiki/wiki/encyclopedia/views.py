from django.shortcuts import render

from . import util, forms

form = forms.searchform()


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": form},
    )


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
                "form": form,
            },
        )


def get_search(request):
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
                return render(
                    request,
                    "encyclopedia/search.html",
                    {"error": "No results found", "form": search},
                )
            elif len(matches) == 1 and matches[0].lower == search:
                # one exact match found, loads wiki/[title]
                match = matches[0]
                return page(request, match)
            else:
                #  multiple matches found, redirect to search.html
                title = [entry for entry in matches if search == entry.lower()]

                if len(title) > 0:
                    return page(request, title[0])
                else:
                    return render(
                        request,
                        "encyclopedia/search.html",
                        {"results": matches, "form": search},
                    )

    # Invalid request, loads index.
    return index(request)

def new(request):
    return render(request, "encyclopedia/new_page.html")