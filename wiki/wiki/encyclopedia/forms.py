from django import forms


class searchform(forms.Form):
    search = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}),
    )


class newpageform(forms.Form):
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
    title = forms.CharField(
        label="Title",
        disabled=False,
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "class": "col-sm-12",
            }
        ),
    )

    body = forms.CharField(
        label="Content",
        required=False,
        widget=forms.Textarea(attrs={"class": "col-sm-11"}),
    )
