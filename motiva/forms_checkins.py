from django import forms

from .models import CheckIn


RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]


def rating_field(label):
    """A 1–5 rating shown as clickable bubbles instead of a free number box."""
    return forms.TypedChoiceField(
        label=label,
        choices=RATING_CHOICES,
        coerce=int,
        widget=forms.RadioSelect(attrs={"class": "scale-input"}),
    )


class CheckInForm(forms.ModelForm):
    confidence = rating_field("I can make progress (1–5)")
    importance = rating_field("This matters to me (1–5)")
    demand = rating_field("This feels demanding (1–5)")

    class Meta:
        model = CheckIn
        fields = ("goal", "barrier", "confidence", "importance", "demand", "available_minutes")
        labels = {
            "goal": "What would you like to work on?",
            "barrier": "What is the main barrier?",
            "confidence": "I can make progress (1–5)",
            "importance": "This matters to me (1–5)",
            "demand": "This feels demanding (1–5)",
            "available_minutes": "Available minutes",
        }
        widgets = {"goal": forms.Textarea(attrs={"rows": 3})}


class ActionForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ("next_action",)
        labels = {"next_action": "My next action"}
        widgets = {"next_action": forms.Textarea(attrs={"rows": 3})}
