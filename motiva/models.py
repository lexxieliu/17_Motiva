from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CheckIn(models.Model):
    class Barrier(models.TextChoices):
        START = "start", "Unsure where to start"
        CONFIDENCE = "confidence", "Low confidence"
        VALUE = "value", "Hard to see the value"
        TIME = "time", "Limited time or energy"
        OTHER = "other", "Something else"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.TextField()
    barrier = models.CharField(max_length=12, choices=Barrier.choices)
    confidence = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    importance = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    demand = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    available_minutes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(180)])
    class SuggestionSource(models.TextChoices):
        AI = "ai", "AI (Gemini)"
        RULE = "rule", "Rule-based"

    next_action = models.TextField()
    suggested_action = models.TextField(blank=True)
    suggestion_source = models.CharField(
        max_length=4, choices=SuggestionSource.choices, default=SuggestionSource.RULE
    )
    ai_strategy = models.CharField(max_length=12, blank=True)
    ai_rationale = models.TextField(blank=True)
    ai_estimated_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    ai_latency_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Reflection(models.Model):
    class Outcome(models.TextChoices):
        COMPLETED = "completed", "Completed"
        PARTIAL = "partial", "Partly completed"
        NOT_STARTED = "not_started", "Not started"

    checkin = models.OneToOneField(CheckIn, on_delete=models.CASCADE, related_name="reflection")
    outcome = models.CharField(max_length=12, choices=Outcome.choices)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
