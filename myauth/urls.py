from django.urls import path
# from . import views
from .views import getlogin
from .views import registeruser
from .views import edituser
from .views import deleteuser
from .views import showuser

urlpatterns = [
    # path('login/', views.getlogin),
path('login/', getlogin),
path('register/', registeruser),
path('edituser/', edituser),
path('deleteuser/', deleteuser),
path('showuser/', showuser),
]
