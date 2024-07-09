from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import WorkoutSession, Exercise, SetDetail
from django.db import IntegrityError    
from django.db import transaction

def index(request): 
    # Initialize profile picture URL as None
    profile_pic_url = None
    
    # Fetch the Google profile picture URL if the user is authenticated
    if request.user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            profile_pic_url = social_account.extra_data.get('picture')
        except SocialAccount.DoesNotExist:
            profile_pic_url = None

    # Pass the URL to the template context
    context = {
        'profile_pic_url': profile_pic_url
    }
    return render(request, 'index.html', context)  # Pass context here

def logout_view(request):
    # if request.user.is_authenticated:
    #     try:
    #         extra_data = SocialAccount.objects.get(user=request.user).extra_data
    #         print(extra_data['picture'])
    #     except SocialAccount.DoesNotExist:
    #         pass
    logout(request)
    return redirect("/")

def loginPage(request):
    return render(request, 'Login.html')

@login_required
def recordWorkout(request):
    profile_pic_url = None
    if request.user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            profile_pic_url = social_account.extra_data.get('picture')
        except SocialAccount.DoesNotExist:
            profile_pic_url = None
    print(f"workout page 2 {profile_pic_url}")
    # Pass the URL to the template context
    context = {
        'profile_pic_url': profile_pic_url
    }
    return render(request, 'WorkoutPage2.html', context)

@csrf_exempt
def handle_url_view(request):
    if request.method == 'POST':
        with transaction.atomic():
            try:
                date = request.POST.get('date')
                if not date:
                    raise ValueError("Date is required.")

                if WorkoutSession.objects.filter(user=request.user, date=date).exists():
                    raise ValueError("Workout session for this date already exists.")

                workout_session = WorkoutSession.objects.create(user=request.user, date=date)

                for workout_num in range(1, 6):
                    exercise_name = request.POST.get(f'workout-{workout_num}-options')
                    if not exercise_name:
                        raise ValueError(f"Exercise name for workout {workout_num} is required.")

                    exercise, created = Exercise.objects.get_or_create(name=exercise_name.strip())

                    for set_num in range(1, 5):
                        weights = request.POST.get(f'workout-{workout_num}-set{set_num}-weights')
                        reps = request.POST.get(f'workout-{workout_num}-set{set_num}-reps')

                        if (weights and not reps) or (reps and not weights):
                            raise ValueError(f"For workout {workout_num}, set {set_num}, both weights and reps must be provided if one is provided.")

                        weights = float(weights) if weights else 0
                        reps = int(reps) if reps else 0

                        SetDetail.objects.create(
                            exercise=exercise,
                            workout_session=workout_session,
                            set_number=set_num,
                            weight=weights,
                            reps=reps
                        )

                # Redirect to the download page for the specific workout session
                return redirect('download', workout_session_id=workout_session.id)
            except ValueError as e:
                # Handle the error (e.g., return an error response or re-render the form with an error message)
                return HttpResponse(str(e))  # Return an error message as HttpResponse

    # Handle GET requests or other cases where POST data is not processed
    return HttpResponse("Method not allowed or invalid request.")
def download_view(request, workout_session_id):
    profile_pic_url = None
    if request.user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            profile_pic_url = social_account.extra_data.get('picture')
        except SocialAccount.DoesNotExist:
            profile_pic_url = None
    print(f"download page {profile_pic_url}")
    # Pass the URL to the template context
    workout_session = get_object_or_404(WorkoutSession, id=workout_session_id, user=request.user)
    set_details = SetDetail.objects.filter(workout_session=workout_session)

    context = {
        'workout_session': workout_session,
        'set_details': set_details,
        'profile_pic_url': profile_pic_url
    }
    return render(request, 'downloadpage.html', context)

def dashboard(request):
    workout_sessions = WorkoutSession.objects.filter(user=request.user).order_by('date')
    return render(request, 'dashboard.html', {'workout_sessions': workout_sessions})