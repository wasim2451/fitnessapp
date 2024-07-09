from django.contrib import admin
from django.urls import path
from fitbuddy import views
urlpatterns = [
    path("", views.index, name="home"),
    path("logout", views.logout_view),
    path("login", views.loginPage, name="loginPage"),
    path("tracker", views.recordWorkout, name="recordWorkout"),
    path("handleSubmit", views.handle_url_view, name="submithandler"),
    path('workout/', views.handle_url_view, name='handle_url'),
    path('download/<int:workout_session_id>/', views.download_view, name='download'),
    path('dashboard', views.dashboard, name='dashboard')
]
