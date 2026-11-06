from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms_reflections import HistorySearchForm, ReflectionForm
from .models import CheckIn, Reflection


@login_required
@require_http_methods(["GET", "POST"])
def reflection_edit(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk, owner=request.user)
    reflection = Reflection.objects.filter(checkin=checkin).first()
    form = ReflectionForm(request.POST if request.method == "POST" else None, instance=reflection)
    if request.method == "POST" and form.is_valid():
        reflection = form.save(commit=False)
        reflection.checkin = checkin
        reflection.save()
        return redirect("history_list")
    return render(request, "motiva/reflection_form.html", {"checkin": checkin, "form": form})


@login_required
@require_http_methods(["GET"])
def history_list(request):
    checkins = CheckIn.objects.filter(owner=request.user).select_related("reflection")
    has_checkins = checkins.exists()
    search_form = HistorySearchForm(request.GET)
    query = ""
    if search_form.is_valid():
        query = search_form.cleaned_data["q"].strip()
        if query:
            checkins = checkins.filter(goal__icontains=query)
    checkins = checkins.order_by("-created_at", "-pk")
    return render(
        request,
        "motiva/history_list.html",
        {"checkins": checkins, "has_checkins": has_checkins, "search_form": search_form, "query": query},
    )
