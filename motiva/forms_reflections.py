from django import forms

from .models import Reflection


class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ("outcome", "notes")
        labels = {"outcome": "How did it go?", "notes": "Notes (optional)"}
        widgets = {
            "outcome": forms.RadioSelect,
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class HistorySearchForm(forms.Form):
    q = forms.CharField(label="Search goals", required=False, max_length=200)
