from django.contrib import admin
from .models import Exercise, WorkoutSession, SetDetail, WorkoutDetail


admin.site.register(Exercise)
admin.site.register(WorkoutSession)
admin.site.register(SetDetail)
admin.site.register(WorkoutDetail)
