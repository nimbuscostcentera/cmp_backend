from django.urls import path
from . import views

urlpatterns = [
    # SetupInfo API
    path('setupinfo/', views.SetupInfoListCreateView.as_view(), name='setupinfo-list-create'),
    path('setupinfo/<int:pk>/', views.SetupInfoDetailView.as_view(), name='setupinfo-detail'),

    # ProcessWiseControl API
    path('processwisecontrol/', views.ProcessWiseControlListCreateView.as_view(), name='processwisecontrol-list-create'),
    path('processwisecontrol/<int:pk>/', views.ProcessWiseControlDetailView.as_view(), name='processwisecontrol-detail'),
]
