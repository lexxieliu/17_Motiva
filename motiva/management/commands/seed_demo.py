"""Create a demo account with realistic past check-ins for the video demo.

    python manage.py seed_demo            # asks for a password
    python manage.py seed_demo --reset    # also clears the demo user's old check-ins

Safe to re-run. Only touches the demo user's own records.
"""
import getpass
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from motiva.models import CheckIn, Reflection

# (days ago, hour, goal, barrier, confidence, importance, demand, minutes,
#  source, strategy, suggestion, est. minutes, rationale, saved action (None = kept suggestion),
#  outcome, notes)
SAMPLES = [
    (6, 19, "Finish the reading for INFO 490 discussion on data ethics", "value", 3, 3, 3, 30,
     "ai", "value",
     "Read the first section of the article and write one sentence on how it relates to your capstone dataset.",
     20, "Linking the reading to your own project gives it a clear purpose before you start.",
     None, "completed", "Connecting it to my project made it way easier to start."),
    (4, 21, "Practice SQL joins for the database quiz on Friday", "confidence", 2, 5, 4, 45,
     "ai", "confidence",
     "Redo two INNER JOIN exercises from last week's lab that you already solved, then try one LEFT JOIN.",
     30, "Starting with problems you've solved before builds confidence before the new material.",
     "Redo two INNER JOIN lab exercises, then try one LEFT JOIN from the practice set.",
     "partial", "Got through the inner joins, LEFT JOIN still confusing. Ask in office hours."),
    (2, 16, "Start the literature review for my research methods paper", "start", 2, 4, 5, 25,
     "ai", "start",
     "Search Google Scholar for one keyword from your topic and save the three most-cited papers.",
     20, "A single search with a fixed number of papers turns a big task into a small first step.",
     None, "completed", "Found 3 good papers in 15 minutes."),
    (1, 22, "Review statistics lecture notes before the midterm", "time", 3, 5, 3, 15,
     "rule", "", "Choose one small step that fits the time you have available.", None, "",
     "Re-read the summary slide on hypothesis testing.", "not_started", "Too tired after work, will do it tomorrow morning."),
]


class Command(BaseCommand):
    help = "Create or refresh the demo account with sample check-ins and reflections."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="demo_student")
        parser.add_argument("--password", help="Password for the demo account (prompted if omitted).")
        parser.add_argument("--reset", action="store_true", help="Delete the demo user's existing check-ins first.")

    @transaction.atomic
    def handle(self, *args, **opts):
        User = get_user_model()
        user, created = User.objects.get_or_create(username=opts["username"])
        if created or opts["password"] or not user.has_usable_password():
            password = opts["password"] or getpass.getpass(f"Password for {user.username}: ")
            if not password:
                raise CommandError("A password is required.")
            user.set_password(password)
            user.save()

        existing = CheckIn.objects.filter(owner=user)
        if opts["reset"]:
            existing.delete()
        elif existing.exists():
            self.stdout.write(f"{user.username} already has check-ins; use --reset to recreate them.")
            return

        now = timezone.now()
        for (days, hour, goal, barrier, conf, imp, dem, minutes, source, strategy, suggestion, est,
             rationale, saved, outcome, notes) in SAMPLES:
            checkin = CheckIn.objects.create(
                owner=user, goal=goal, barrier=barrier, confidence=conf, importance=imp, demand=dem,
                available_minutes=minutes, suggestion_source=source, suggested_action=suggestion,
                ai_strategy=strategy, ai_rationale=rationale, ai_estimated_minutes=est,
                ai_latency_ms=1400 + days * 90 if source == "ai" else None,
                next_action=saved or suggestion,
            )
            when = (now - timedelta(days=days)).replace(hour=hour, minute=12, second=0, microsecond=0)
            CheckIn.objects.filter(pk=checkin.pk).update(created_at=when)
            reflection = Reflection.objects.create(checkin=checkin, outcome=outcome, notes=notes)
            Reflection.objects.filter(pk=reflection.pk).update(created_at=when + timedelta(hours=1))

        self.stdout.write(self.style.SUCCESS(
            f"{'Created' if created else 'Updated'} {user.username} with {len(SAMPLES)} sample check-ins."
        ))
