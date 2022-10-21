from django import forms


class searchform(forms.Form):
    """
    Form model for search bar
    """

    search = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}),
    )


class newpageform(forms.Form):
    """
    Form model for creation of new entry
    """

    title = forms.CharField(
        label="Title",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Page Title...", "class": "col-sm-11"}
        ),
    )

    body = forms.CharField(
        label="Content",
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Markdown Content...", "class": "col-sm-11"}
        ),
    )


class editpageform(forms.Form):
    """
    Form model for editing of entry
    """

    title = forms.CharField(label="Title", required=False, widget=forms.HiddenInput())

    body = forms.CharField(
        label="Content",
        required=False,
        widget=forms.Textarea(attrs={"class": "col-sm-11"}),
    )
