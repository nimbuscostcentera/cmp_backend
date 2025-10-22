from django.urls import path
from .views import OpeningList

urlpatterns = [
    path("openings/", OpeningList.as_view(), name="opening-list"),
    path("openings/<int:pk>/", OpeningList.as_view(), name="opening-list"),
]
