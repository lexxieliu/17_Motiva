from django import forms

from .models import CheckIn


class CheckInForm(forms.ModelForm):
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
