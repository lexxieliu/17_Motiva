from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .ai_suggestions import Suggestion, validate
from .models import CheckIn

CHECKIN_DATA = {
    "goal": "Review chapter 4 for the chemistry midterm",
    "barrier": "start",
    "confidence": 2,
    "importance": 5,
    "demand": 4,
    "available_minutes": 25,
}


class ValidateTests(TestCase):
    def good(self, **overrides):
        data = {"strategy": "start", "action": "Open the slides.", "estimated_minutes": 10, "rationale": "Small start."}
        data.update(overrides)
        return data

    def test_accepts_valid_output(self):
        self.assertEqual(validate(self.good(), 25)["estimated_minutes"], 10)

    def test_rejects_unknown_strategy(self):
        with self.assertRaises(ValueError):
            validate(self.good(strategy="nap"), 25)

    def test_rejects_minutes_over_available_time(self):
        with self.assertRaises(ValueError):
            validate(self.good(estimated_minutes=60), 25)

    def test_rejects_empty_action(self):
        with self.assertRaises(ValueError):
            validate(self.good(action="  "), 25)


class CheckInSuggestionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("student", password="pw-12345")
        self.client.force_login(self.user)

    @mock.patch("motiva.views_checkins.ai_suggestions.suggest_action")
    def test_ai_suggestion_is_saved_and_shown(self, suggest):
        suggest.return_value = Suggestion(
            strategy="start",
            action="Open the Chapter 4 slides and write three notes on reaction rates.",
            estimated_minutes=15,
            rationale="One source and a fixed number of notes make it easy to begin.",
            latency_ms=900,
        )
        response = self.client.post(reverse("checkin_create"), CHECKIN_DATA, follow=True)
        checkin = CheckIn.objects.get()
        self.assertEqual(checkin.suggestion_source, "ai")
        self.assertEqual(checkin.next_action, suggest.return_value.action)
        self.assertEqual(checkin.ai_latency_ms, 900)
        self.assertContains(response, "AI suggestion")

    @mock.patch("motiva.views_checkins.ai_suggestions.suggest_action", return_value=None)
    def test_falls_back_to_rule_based_action(self, suggest):
        response = self.client.post(reverse("checkin_create"), CHECKIN_DATA, follow=True)
        checkin = CheckIn.objects.get()
        self.assertEqual(checkin.suggestion_source, "rule")
        self.assertEqual(checkin.next_action, "Choose one source and write three notes.")
        self.assertContains(response, "Rule-based suggestion")

    @mock.patch.dict("os.environ", {"GEMINI_API_KEY": ""})
    def test_missing_key_still_saves_checkin(self):
        self.client.post(reverse("checkin_create"), CHECKIN_DATA)
        self.assertEqual(CheckIn.objects.get().suggestion_source, "rule")


class RatingInputTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("student2", password="pw-12345")
        self.client.force_login(self.user)

    def test_ratings_render_as_radio_buttons(self):
        response = self.client.get(reverse("checkin_create"))
        self.assertContains(response, 'type="radio" name="confidence" value="5"')

    @mock.patch("motiva.views_checkins.ai_suggestions.suggest_action", return_value=None)
    def test_rating_above_five_is_rejected(self, suggest):
        response = self.client.post(reverse("checkin_create"), {**CHECKIN_DATA, "importance": 10})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CheckIn.objects.exists())


class SeedDemoTests(TestCase):
    def test_seed_demo_creates_user_and_history(self):
        from django.core.management import call_command

        call_command("seed_demo", password="demo-pass-123", stdout=open("/dev/null", "w"))
        user = get_user_model().objects.get(username="demo_student")
        self.assertTrue(user.check_password("demo-pass-123"))
        self.assertEqual(CheckIn.objects.filter(owner=user).count(), 4)
        self.client.force_login(user)
        response = self.client.get(reverse("history_list"))
        self.assertContains(response, "SQL joins")
