from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms_checkins import ActionForm, CheckInForm
from .models import CheckIn


BASELINE_ACTIONS = {
    CheckIn.Barrier.START: "Choose one source and write three notes.",
    CheckIn.Barrier.CONFIDENCE: "Identify one familiar part of the task and attempt it.",
    CheckIn.Barrier.VALUE: "Write one sentence connecting the task to a personal goal.",
    CheckIn.Barrier.TIME: "Choose one small step that fits the time you have available.",
    CheckIn.Barrier.OTHER: "Choose and describe one manageable first step.",
}


@login_required
@require_http_methods(["GET", "POST"])
def checkin_create(request):
    form = CheckInForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        checkin = form.save(commit=False)
        checkin.owner = request.user
        checkin.next_action = BASELINE_ACTIONS[checkin.barrier]
        checkin.save()
        return redirect("checkin_detail", pk=checkin.pk)
    return render(request, "motiva/checkin_form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def checkin_detail(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk, owner=request.user)
    form = ActionForm(request.POST if request.method == "POST" else None, instance=checkin)
    if request.method == "POST" and form.is_valid():
        checkin.save(update_fields=["next_action"])
        return redirect("checkin_detail", pk=checkin.pk)
    return render(
        request,
        "motiva/checkin_detail.html",
        {"checkin": checkin, "form": form, "baseline_action": BASELINE_ACTIONS[checkin.barrier]},
    )
