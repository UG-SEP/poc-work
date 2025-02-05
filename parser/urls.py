from django.urls import path
from .views import extract_resume

urlpatterns = [
    path('', extract_resume, name='extract-resume'),
]
