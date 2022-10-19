from django import forms


class searchform(forms.Form):
    search = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}),
    )
