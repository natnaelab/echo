from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile_view(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, "users/profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form})
